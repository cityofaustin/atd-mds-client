"""
Class: MDSClient040

Author: Austin Transportation Department, Data and Technology Services

Description: The purpose of this class is to provide an extension of the MDSClientBase
class that is compatible with version 0.4.X of the Mobility Data Specification (MDS).
https://github.com/openmobilityfoundation/mobility-data-specification/tree/master/provider

The application requires the requests library:
    https://pypi.org/project/requests/
"""
from datetime import datetime, timezone
from .MDSClientBase import MDSClientBase

# Debug & Logging
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MDSClient040(MDSClientBase):
    version = "0.4.0"

    # Specify the name for each parameter:
    # param_schema = {
    #   param_name_in_configuration: param_name_in_mds_v0_3_0
    # }

    # Parameters based on this documentation:
    # https://github.com/openmobilityfoundation/mobility-data-specification/tree/0.3.x/provider#trips-query-parameters
    param_schema = {
        "start_time": "start_time",
        "end_time": "end_time",
        "bbox": "bbox",
        "device_id": "device_id",
        "vehicle_id": "vehicle_id",
    }

    def __init__(self, config):
        MDSClientBase.__init__(self, config)

    @staticmethod
    def _has_trips(data):
        """
        Returns True if the data contains trips
        :param dict data: The response data as provided by self.__request
        :return bool:
        """
        return len(data.get("payload", {}).get("data", {}).get("trips", [])) > 0

    @staticmethod
    def _has_data(data):
        """
        Returns True if data has any valid content.
        :param dict data: The response data as provided by self.__request
        :return bool:
        """
        return len(data.get("payload", {}).get("data", {})) > 0

    @staticmethod
    def _has_next_link(data):
        """
        Returns true if data contains a valid link to the next page
        :param dict data: The response data as provided by self.__request
        :return bool:
        """
        return True if data.get("payload", {}).get("links", {}).get("next", None) else False

    @staticmethod
    def _get_next_link(data):
        """
        Returns the link for the next page
        :param dict data: The response data as provided by self.__request
        :return bool:
        """
        return data.get("payload", {}).get("links", {}).get("next", None)

    def _get_response_version(self, data):
        """
        Returns the MDS version number as provided in the response body
        :param dict data: The response data as provided by self.__request
        :return str: The version number as provided by the mds endpoint response
        """
        return data.get("payload", {}).get("version", self.version)

    @staticmethod
    def _adjust_time(time):
        """
        Returns the same time in unix timestamp minus one hour.
        :param int time: the unix epoch time to be adjusted
        :return int:
        """
        return time - 3600

    @staticmethod
    def _convert_format(time):
        """
        Turns a unix epoch timestamp into a date "yyyy-mm-ddYhh" format.
        :param int time: the unix epoch time to be converted
        :return str:
        """
        return datetime.fromtimestamp(time, tz=timezone.utc).strftime("%Y-%m-%dT%H")

    def get_trips(
        self, end_time, **kwargs,
    ):
        """
        Returns a JSON dictionary with a list of all
        :param int end_time: The end time in unix format
        :param str vehicle_id: (Optional) The vehicle ID
        :param str bbox: (Optional) Specify a bounding box (e.g., bbox="-122.4183,37.7758,-122.4120,37.7858")
        :param bool paging: (Optional) An override to paging. Set to True to enable it.
        :return dict:
        """
        logging.debug("MDSClient040::get_trips() Getting trips: %s " % (end_time))

        self._load_params(end_time=end_time, **kwargs)

        # Out trips accumulator
        trips_accumulator = []
        # Contains our MDS endpoint with /trips path
        current_endpoint = f"{self.mds_endpoint}/trips"
        # A flag whose value is True if there is more data to download
        has_next_link = False

        # Start an endless loop
        while True:

            # 1. Make the HTTP Request
            data = self._request(
                mds_endpoint=current_endpoint,
                headers=self.headers,
                params=None if has_next_link else self.params,
            )

            # 2. Check if we have a next link
            has_next_link = self._has_next_link(data)

            # 3. If the data has trips, process them.
            if self._has_trips(data):
                # Gather the trips from `data`
                trips = data["payload"]["data"]["trips"]
                # Append the trips to the current list
                trips_accumulator += trips
                # Wipe out the current trips variable and start over
                trips = None

            # 4. Quit loop if not paging
            if self.paging is False:
                logging.debug(
                    "MDSClient040::get_trips() Paging set to False, stopping request..."
                )
                break

            # 5. The `next` link becomes our new endpoint
            current_endpoint = self._get_next_link(data)

            # 6. If the endpoint is None, then quit loop
            if current_endpoint:
                logging.debug(
                    "MDSClient040::get_trips() Next link: %s" % current_endpoint
                )
            else:
                break

        # Return trips in this envelope:
        return {
            "version": self._get_response_version(data),
            "data": {"trips": trips_accumulator},
        }

    def _load_params(self, end_time, **kwargs):
        """
        Takes the parameters from the configuration and start time
        and loads them into our self.params dictionary.
        :param int end_time: The hour we need data for (as specified in MDS 0.4.0)
        :param dict kwargs: Any additional parameters to be taken as HTTP param.
        :return:
        """

        final_end_time = self._convert_format(
            time=self._adjust_time(
                time=end_time
            )
        )

        params = {**{"end_time": final_end_time, **kwargs}}

        # Set the required URI parameters
        for key, value in params.items():
            self.params[self.param_schema[key]] = value

        # Delete the end_time parameter (if present)
        if "start_time" in self.params:
            del self.params["start_time"]
