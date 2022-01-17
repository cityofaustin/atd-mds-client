#!/usr/bin/env python

# Required Libraries
import json

from parent_directory import *
from mds.MDSAuth import MDSAuth


class TestMDSAuth:
    config = None

    def setup_class(self):
        print("\n\n---------------------------------------------")
        print("Beginning tests for: TestMDSAuth")
        print("---------------------------------------------")
        with open("tests/config.json", "r") as json_file:
            self.config = json.load(json_file)

        if isinstance(self.config, dict) is False:
            raise Exception("Configuration file 'tests/config.json' could not be loaded.")

    def teardown_class(self):
        print("\n\n---------------------------------------------")
        print("All tests finished for: TestMDSAuth")
        print("---------------------------------------------")
        self.config = None

    def test_constructor_success_t1(self):
        """
        Tests if the auth_client is initialized and authenticate is callable method
        """
        auth_client = MDSAuth(
            config=self.config["lime"], custom_function=None
        )
        assert isinstance(auth_client, MDSAuth) and \
            callable(auth_client.authenticate)

    def test_constructor_success_t2(self):
        """
        Tests if the auth_client is initialized and authenticate is callable method
        """
        auth_client = MDSAuth(
            config=self.config["lyft"], custom_function=None
        )
        assert isinstance(auth_client, MDSAuth) and \
               callable(auth_client.authenticate)

    def test_mds_oauth_success_t1(self):
        """
        Tests mds_oauth and checks if the client's headers are initialized
        """
        auth_client = MDSAuth(
            config=self.config["free2move"], custom_function=None
        )
        auth_client.mds_oauth()
        assert isinstance(auth_client.headers, dict) and \
            len(auth_client.headers.get("Authorization", "")) > 16

    def test_mds_auth_token_success_t1(self):
        """
        Tests mds_auth_token and checks if the client's headers are initialized
        """
        auth_client = MDSAuth(
            config=self.config["bird"], custom_function=None
        )
        auth_client.mds_auth_token()
        assert isinstance(auth_client.headers, dict) and \
            len(auth_client.headers.get("Authorization", "")) > 16

    def test_mds_http_basic_success_t1(self):
        """
        Tests mds_http_basic and checks if the client's headers are initialized
        """
        auth_client = MDSAuth(
            config=self.config["lyft"], custom_function=None
        )
        auth_client.mds_http_basic()
        assert isinstance(auth_client.headers, dict) and \
            len(auth_client.headers.get("Authorization", "")) > 16

    def test_mds_custom_auth_success_t1(self):
        """
        Tests mds_custom_auth and checks if client's headers are initialized
        by the custom function we provided.
        """
        def custom_auth(config):
            return {
                "Authorization": "Bearer abc123"
            }

        auth_client = MDSAuth(
            config=self.config["sample_co"], custom_function=custom_auth
        )
        auth_client.mds_custom_auth()
        assert isinstance(auth_client.headers, dict) and \
            auth_client.headers.get("Authorization", "") == "Bearer abc123"
