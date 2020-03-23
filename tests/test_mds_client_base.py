#!/usr/bin/env python

# Required Libraries
import json
from parent_directory import *

from mds.clients.MDSClientBase import MDSClientBase


class DummyResponse:
    status_code = 200
    content = "This is some sample content"

    @staticmethod
    def json():
        return {
            "This is the content"
        }

class TestMDSBase:
    mds_config = None
    mds_base = None
    mds_dummy_response = None

    def setup_class(self):
        print("\n\n---------------------------------------------")
        print("Beginning tests for: TestMDSBase")
        print("---------------------------------------------")
        with open("tests/config.json", "r") as json_file:
            self.mds_config = json.load(json_file)

        if isinstance(self.mds_config["sample_co"], dict) is False:
            raise Exception("Configuration file 'tests/config.json' could not be loaded.")

        self.mds_base = MDSClientBase(config=self.mds_config["sample_co"])
        self.mds_base.param_schema = {}

    def teardown_class(self):
        print("\n\n---------------------------------------------")
        print("All tests finished for: TestMDSBase")
        print("---------------------------------------------")
        self.mds_config = None
        self.mds_base = None

    def test_constructor_success_t1(self):
        """
        Tests the constructor with a valid configuration
        """
        assert isinstance(self.mds_base, MDSClientBase)

    def test_constructor_fail_t1(self):
        """
        Tests that the constructor fails at the lack of a configuration
        """
        try:
            MDSClientBase(config=None)
            assert False
        except:
            assert True

    def test_build_response_success_t1(self):
        """
        Tests the build response method with a dummy response
        """
        response = self.mds_base._build_response(response=DummyResponse())
        assert isinstance(response, dict) and \
            "status_code" in response and \
            "response" in response and \
            "message" in response and \
            "payload" in response

    def test_set_header_success_t1(self):
        """
        Tests the set header method
        """
        self.mds_base.set_header(key="Test", value="Header")
        assert isinstance(self.mds_base.headers, dict) and \
            self.mds_base.headers.get("Test", "") == "Header"

    def test_set_header_success_t2(self):
        """
        Tests the set header method
        """
        self.mds_base.set_header(key="Second", value="Test")
        assert isinstance(self.mds_base.headers, dict) and \
            self.mds_base.headers.get("Test", "") == "Header" and \
            self.mds_base.headers.get("Second", "") == "Test"

    def test_get_headers_success_t1(self):
        """
        Tests the get headers method
        """
        headers = self.mds_base.get_headers()
        assert isinstance(headers, dict) and \
            headers.get("Test", "") == "Header" and \
            headers.get("Second", "") == "Test"

    def test_render_settings_success_t1(self):
        """
        Tests the render settings method
        """
        self.mds_base.render_settings(headers={
            "Third": "Test"
        })

        assert isinstance(self.mds_base.headers, dict) and \
            self.mds_base.headers.get("Test", "") == "Header" and \
            self.mds_base.headers.get("Second", "") == "Test" and \
            self.mds_base.headers.get("Third", "") == "Test" and \
            self.mds_base.param_schema.get("start_time") == "custom_start_time"

    def test_set_paging_success_t1(self):
        """
        Tests the set paging method
        """
        self.mds_base.set_paging(paging=True)
        assert self.mds_base.paging is True

    def test_set_paging_success_t2(self):
        """
        Tests the set paging method
        """
        self.mds_base.set_paging(paging=False)
        assert self.mds_base.paging is False

    def test_set_delay_success_t1(self):
        """
        Tests the set delay method
        """
        self.mds_base.set_delay(delay=0)
        assert self.mds_base.delay == 0

    def test_set_delay_success_t2(self):
        """
        Tests the set delay method
        """
        self.mds_base.set_delay(delay=1000)
        assert self.mds_base.delay == 1000

    def test_set_timeout_success_t1(self):
        """
        Tests the set timeout method
        """
        self.mds_base.set_timeout(timeout=0)
        assert self.mds_base.timeout == 0

    def test_set_timeout_success_t2(self):
        """
        Tests the set timeout method
        """
        self.mds_base.set_timeout(timeout=1000)
        assert self.mds_base.timeout == 1000

    def test_set_max_attempts_success_t1(self):
        """
        Tests the set max attempts method
        """
        self.mds_base.set_max_attempts(max_attempts=0)
        assert self.mds_base.max_attempts == 0

    def test_set_max_attempts_success_t2(self):
        """
        Tests the set max attempts method
        """
        self.mds_base.set_max_attempts(max_attempts=1000)
        assert self.mds_base.max_attempts == 1000
