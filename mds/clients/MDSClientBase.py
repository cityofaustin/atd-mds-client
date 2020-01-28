"""
Class: MDSClientBase

Author: Austin Transportation Department, Data and Technology Services

Description: The purpose of this class is to provide a blueprint design
and basic shared functionality for all derived MDS classes.

The application requires the requests library:
    https://pypi.org/project/requests/
"""

import time
import requests

# Debug & Logging
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MDSClientBase:

    __slots__ = (
        "config",
        "params",
        "headers",
        "param_schema",
        "mds_endpoint",
        "paging",
        "delay",
        "timeout",
        "max_attempts",
    )

    def __init__(self, config):
        self.config = config
        self.headers = {}
        self.params = {}
        self.mds_endpoint = self.config.get("mds_api_url", None)
        self.paging = self.config.get("paging", True)
        self.delay = self.config.get("delay", 0)
        self.timeout = self.config.get("interval", None)
        self.max_attempts = self.config.get("max_attempts", 3)

    @staticmethod
    def _build_response(response):
        """
        Builds a data payload to be given back to the client
        :param object response: As provided by requests.get
        :return dict: A parsed response data
        """

        # In the future, we may want to refactor this
        # to handle 301 and 302 redirect responses.
        status_code = response.status_code if hasattr(response, "status_code") else -1
        success = status_code == 200
        message = response.content if hasattr(response, "content") else "No response message provided."

        logging.debug(
            f"MDSClientBase::_build_response() status_code: {status_code}"
        )

        return {
            "status_code": status_code,
            "response": "success" if success else "error",
            "message": "success" if success else f"Error: {message}",
            "payload": response.json() if success else {},
        }

    def _request(self, mds_endpoint, **kwargs):
        """
        Makes an HTTP request
        :param str mds_endpoint: The URL endpoint to make the request to
        :param dict params: (Optional) URI Parameters to add to the request
        :param dict headers: (Optional) A dictionary of HTTP headers to pass to the request
        :return dict:
        """
        logging.debug(f"\nMDSClientBase::__request() Making request...")

        # Load our endpoint, parameters and headers
        mds_params = kwargs.get("params", {})
        mds_headers = kwargs.get("headers", {})

        # Manage our current attempt to make an HTTP request
        current_attempts = 0

        # Log our current values
        logging.debug(f"MDSClientBase::__request() Details:")
        logging.debug(f"MDSClientBase::__request() mds_endpoint: {mds_endpoint}")
        logging.debug(f"MDSClientBase::__request() mds_params: {mds_params}")
        logging.debug(f"MDSClientBase::__request() mds_headers: {mds_headers}\n")

        # We are going to try N times as specified in self.max_attempts
        while True:
            # Increase current attempt
            current_attempts += 1

            # Wait N seconds as specified in `self.delay`
            time.sleep(self.delay)

            # Let's try to make an HTTP request
            try:
                logging.debug(
                    "MDSClientBase::__request() Attempting request: %s/%s -- Timeout %s, Paging: %s, Delay: %s"
                    % (
                        current_attempts, self.max_attempts, self.timeout, self.paging, self.delay
                    )
                )
                # Make actual request
                response = requests.get(
                    mds_endpoint,
                    params=mds_params,
                    headers=mds_headers,
                    timeout=self.timeout,
                )
                # Build a data json response
                data = self._build_response(response)

            # There was an exception, timeout or otherwise:
            except Exception as e:
                logging.debug(
                    "MDSClientBase::__request() Exception detected: %s" % (str(e))
                )
                data = {
                    "status_code": -1,
                    "response": "error",
                    "message": f"Error: {str(e)}",
                    "payload": {},
                }

            success = data.get("response", "error") == "success"
            logging.debug(
                "MDSClientBase::__request() Reported status: %s" % success
            )

            # Check if we have an error
            if success:
                break
            else:
                # First, log the response error
                logging.debug(
                    "MDSClientBase::__request() Unable to make request: %s"
                    % (data.get("message", "No error message provided"))
                )
                # Check if we still have attempts left
                if current_attempts < self.max_attempts:
                    continue  # Try again in next iteration
                else:
                    # We need to stop the execution, it seems we have a problem
                    raise Exception(
                        "Max attempts reached (%s): could not fetch MDS data at endpoint '%s'"
                        % (self.max_attempts, mds_endpoint)
                    )

        return data

    def set_header(self, key, value):
        """
        Adds an HTTP header to the list
        :param str key: The name of the header
        :param str value: The value of the HTTP header
        """
        logging.debug(
            f"MDSClientBase::set_header() Set header k: '{key}', v: '{value}'"
        )
        self.headers[key] = value

    def render_settings(self, headers={}):
        """
        Compiles the headers and the parameters
        :param dict headers: (Optional) Adds any additional headers to the list (e.g., authentication headers)
        """
        # 1. Consolidate current headers and new headers
        logging.debug("MDSClientBase::render_settings() Rendering headers")
        self.headers = {**self.headers, **headers}

        # 2. Initialize Param Schema & Overrides
        logging.debug("MDSClientBase::render_settings() Rendering parameters")
        params_override = self.config.get("mds_param_override", None)
        if isinstance(params_override, dict):
            for key, value in params_override.items():
                self.param_schema[key] = value

    def get_headers(self):
        """
        Returns the current list of headers
        :return dict:
        """
        return self.headers

    def set_paging(self, paging):
        """
        Allows to override the paging configuration
        :param bool paging: The new paging configuration. True to enable paging.
        """
        self.paging = paging

    def set_delay(self, delay):
        """
        Allows to override the paging configuration
        :param int delay: The new delay setting in seconds.
        """
        self.delay = delay

    def set_timeout(self, timeout):
        """
        Allows to override the paging configuration
        :param int timeout: The new timeout in seconds.
        """
        self.timeout = timeout

    def set_max_attempts(self, max_attempts):
        """
        Allows to override the max_attempts configuration
        :param int max_attempts: The new max_attempts setting.
        """
        self.max_attempts = max_attempts
