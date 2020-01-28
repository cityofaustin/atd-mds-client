"""

"""

import base64
import requests
# Debug & Logging
import logging


class MDSAuth:
    __slots__ = (
        "config",
        "oauth_token",
        "session",
        "headers",
        "authenticate",
        "custom_function",
    )

    def __init__(self, config, custom_function=None):
        """
        Initializes the class and the internal configuration
        :param dict config:
        :param function custom_function: A python function to run as a custom authentication
        """
        self.config = config
        self.custom_function = custom_function
        auth_type = self.config.get("auth_type", None)
        self.headers = None

        if auth_type:
            logging.debug(f"MDSAuth::__init__() Authentication method: {auth_type}")
            self.authenticate = {
                "oauth": self.mds_oauth,
                "bearer": self.mds_auth_token,
                "basic": self.mds_http_basic,
                "custom": self.mds_custom_auth,
            }.get(auth_type.lower(), None)

            if not self.authenticate:
                raise Exception(
                    f"MDSAuth::__init__() Invalid authentication method provided, auth_type: '{auth_type}'"
                )
        else:
            raise Exception(
                f"MDSAuth::__init__() No authentication method provided, auth_type: '{auth_type}'"
            )

    def mds_oauth(self):
        logging.debug("MDSAuth::mds_oauth() Running OAuth authentication")
        auth_data = self.config.get("auth_data", {})
        token_url = self.config.get("token_url", None)

        logging.debug("MDSAuth::mds_oauth() Making OAuth HTTP Request...")
        if token_url:
            response = requests.post(token_url, data=auth_data)
        else:
            raise Exception(
                "MDSAuth::mds_oauth() No token_url defined in the settings."
            )

        auth_token_res_key = self.config.get("auth_token_res_key", None)
        if auth_token_res_key:
            token = response.json().get(auth_token_res_key, None)
        else:
            raise Exception(
                "MDSAuth::mds_oauth() 'auth_token_res_key' is "
                "not defined in the config, usually set to 'jwt' or 'access_token'."
            )

        if token:
            logging.debug("MDSAuth::mds_oauth() Received token: %s[...]" % (token[:6]))
            self.headers = {"Authorization": f"Bearer {token}"}

            return self.headers
        else:
            raise Exception("MDSAuth::mds_oauth() Token could not be resolved.")

    def mds_auth_token(self):
        logging.debug("MDSAuth::mds_auth_token() Running Token authentication")
        self.headers = {"Authorization": f'Bearer {self.config["token"]}'}
        return self.headers

    def mds_http_basic(self):
        logging.debug("MDSAuth::mds_oauth() Running HTTP Basic authentication")
        auth_data = self.config.get("auth_data", None)
        if auth_data:
            username = auth_data.get("username", None)
            password = auth_data.get("password", None)
            encoded_creds = base64.b64encode(
                f"{username}:{password}".encode("utf-8")
            ).decode("utf-8")
            self.headers = {"Authorization": f"Basic {encoded_creds}"}
            return self.headers
        else:
            raise Exception("No credentials provided")

        return None

    def mds_auth_custom(self):
        logging.debug("MDSAuth::mds_oauth() Running Custom authentication")
        pass

    def mds_custom_auth(self):
        return self.custom_function(self.config)

    def _gather_oauth_token(self):
        logging.debug("MDSAuth::_gather_oauth_token() Gathering OAuth token")
        pass