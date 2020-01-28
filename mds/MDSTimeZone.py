"""
Class: MDSTimeZone

Author: Austin Transportation Department, Data and Technology Services

Description: The purpose of this class is to generate time-zone aware
python date-times that can be passed to the MDS client.

The application requires the pytz library:
    https://pypi.org/project/pytz/
"""

from datetime import datetime, timedelta
import pytz


class MDSTimeZone:
    def __init__(
        self,
        date_time_now,
        time_zone=None,
        offset=86400,
        **kwargs
    ):
        """
        Class Constructor
        :param datetime date_time_now: The date time that is to be considered the reference time.
        :param str time_zone: The timezone to be applied to the date time object.
        :param int offset: In seconds, how far back to look for.
        :param dict kwargs: Any other additional parameters
        """

        if time_zone is not None:
            self.time_zone = pytz.timezone(time_zone)

        self.time_start = self.get_time(
            offset=offset,
            date_time_now=date_time_now
        )

        self.time_end = self.get_time(
            date_time_now=date_time_now
        )

        # Any other values or overrides
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_time(self, offset=0, date_time_now=datetime.now()):
        """
        Builds a time object
        :param int offset:The offset to be applied in seconds
        :param datetime date_time_now: The date time object to use, or default to now.
        :return:
        """

        # If the offset is positive, the delta is negative (go back in time)
        # Else, the delta is positive (we go forward in time)
        offset_delta = (
            date_time_now - timedelta(seconds=offset)
            if offset > 0
            else date_time_now + timedelta(seconds=offset)
        )

        # If the offset is 0, then assume the value of date_time_now
        time = (
            date_time_now if offset == 0 else offset_delta
        )

        # Build a timezone-aware date time
        return self.time_zone.localize(time)

    def get_time_start(self, utc=False, unix=False):
        """
        Generates the start timestamp for a query.
        :param bool utc: If True, returns the timestamp in UTC timezone.
        :param bool unix: If True, returns the timestamp in UNIX Epoch format.
        :return:
        """
        # Try to get the time_end attribute from this class, or assume zero
        tz_aware_time_start = getattr(self, "time_start", 0)
        # Use current timezone or UTC if indicated
        tz_aware_output = tz_aware_time_start.astimezone(pytz.UTC) if utc else tz_aware_time_start
        # Use current format, or Unix Epoch if indicated
        return tz_aware_output.timestamp() if unix else tz_aware_output

    def get_time_end(self, utc=False, unix=False):
        """
        Generates the end timestamp for a query.
        :param bool utc: If True, returns the timestamp in UTC timezone.
        :param bool unix: If True, returns the timestamp in UNIX Epoch format.
        :return:
        """
        # Try to get the time_end attribute from this class, or assume zero
        tz_aware_time_end = getattr(self, "time_end", 0)
        # Use current timezone or UTC if indicated
        tz_aware_output = tz_aware_time_end.astimezone(pytz.UTC) if utc else tz_aware_time_end
        # Use current format, or Unix Epoch if indicated
        return tz_aware_output.timestamp() if unix else tz_aware_output
