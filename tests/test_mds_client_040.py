#!/usr/bin/env python

# Required Libraries
import json
from parent_directory import *
from mds.MDSClient import MDSClient


class TestMDS040:
    config = None
    client = None

    def setup_class(self):
        print("\n\n---------------------------------------------")
        print("Beginning tests for: TestMDS040")
        print("---------------------------------------------")
        with open("tests/config.json", "r") as json_file:
            self.config = json.load(json_file)

        if isinstance(self.config, dict) is False:
            raise Exception("Configuration file 'tests/config.json' could not be loaded.")

        self.client = MDSClient(config=self.config["lime"])

    def teardown_class(self):
        print("\n\n---------------------------------------------")
        print("All tests finished for: TestMDS040")
        print("---------------------------------------------")
        self.config = None
        self.client = None

    def test_constructor_success_t1(self):
        """
        Tests if the client initialized correctly.
        """
        assert isinstance(self.client, MDSClient)

    def test_constructor_fail_t1(self):
        """
        Tests if the client fails at the lack of a configuration.
        """
        try:
            MDSClient(config=None)
            assert False
        except:
            assert True

    def test_adjust_time_success_t1(self):
        """
        Tests the adjust time method
        """
        assert self.client.mds_client._adjust_time(time=1578783600) == 1578780000

    def test_convert_time_success_t1(self):
        """
        Tests the convert format method
        """
        assert self.client.mds_client._convert_format(time=1578783600) == "2020-01-11T23"

    def test_schema_success_t1(self):
        """
        Tests if the load_params value provides the correct schema
        """
        self.client.mds_client._load_params(
            end_time=1578783600
        )
        valid_schema = (
                "end_time" in self.client.mds_client.params and
                "start_time" not in self.client.mds_client.params
        )
        assert valid_schema

    def test_params_success_t1(self):
        """
        Tests if the parameters are valid
        """
        valid_params = (
                "end_time" in self.client.mds_client.params and
                "start_time" not in self.client.mds_client.params and
                self.client.mds_client.params["end_time"] == "2020-01-11T22"
        )
        assert valid_params

    def test_get_trips_success_t1(self):
        """
        Tests if the trips response includes version 0.4.0
        """
        trips = self.client.get_trips(
            end_time=1578783600,
            start_time=None
        )
        trips_version = trips.get("version")
        assert isinstance(trips, dict) and \
            trips_version is not None and \
            (trips_version[0:3] == "0.4")
