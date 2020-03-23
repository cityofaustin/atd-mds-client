#!/usr/bin/env python

# Required Libraries
import json
import pdb
from datetime import datetime, timezone, timedelta

from parent_directory import *
from mds.MDSTimeZone import MDSTimeZone


class TestMDSTimeZone:
    tz_time = None
    client = None
    date_time_now = None

    def setup_class(self):
        print("\n\n---------------------------------------------")
        print("Beginning tests for: TestMDSTimeZone")
        print("---------------------------------------------")
        self.date_time_now = datetime(
            2020,  # year
            1,  # month
            11,  # day
            17,  # hour of day
        )
        self.tz_time = MDSTimeZone(
            date_time_now=self.date_time_now,
            offset=3600,
            time_zone="US/Central",
        )

    def teardown_class(self):
        print("\n\n---------------------------------------------")
        print("All tests finished for: TestMDSTimeZone")
        print("---------------------------------------------")
        self.config = None
        self.client = None

    def test_constructor_success_t1(self):
        """
        Tests if the tz_time attribute is an MDSTimeZone Object
        """
        assert isinstance(self.tz_time, MDSTimeZone)

    def test_constructor_timezone_success_t1(self):
        """
        Checks the timezone of the datetime is US/Central
        """
        assert str(self.tz_time.time_zone) == "US/Central"

    def test_constructor_time_start_success_t1(self):
        """
        Checks if the constructor can populate the proper time start
        """
        dt_now_naive = self.date_time_now.replace(tzinfo=None)
        time_start_naive = self.tz_time.time_start.replace(tzinfo=None)
        assert (dt_now_naive - time_start_naive).seconds == 3600

    def test_constructor_time_end_success_t1(self):
        """
        Checks if the constructor can populate the proper time start
        """
        dt_now_naive = self.date_time_now.replace(tzinfo=None)
        time_end_naive = self.tz_time.time_end.replace(tzinfo=None)
        assert (dt_now_naive - time_end_naive).seconds == 0

    def test_get_datetime_success_t1(self):
        """
        Tests if the get_datetime function returns a datetime object
        """
        dt = self.tz_time.get_time()
        assert isinstance(dt, datetime)

    def test_get_datetime_success_t2(self):
        """
        Tests the datetime offset equivalent to one hour
        """
        time_now = datetime.now()
        dt = self.tz_time.get_time(
            offset=3600,
            date_time_now=time_now
        ).replace(tzinfo=None)  # We have to make it a 'naive' datetime
        # We now check the difference is equivalent to the offset we provided
        assert (time_now - dt).seconds == 3600

    def test_get_datetime_success_t3(self):
        """
        Tests the datetime offset equivalent to two hours
        """
        time_now = datetime.now()
        dt = self.tz_time.get_time(
            offset=7200,
            date_time_now=time_now
        ).replace(tzinfo=None)  # We have to make it a 'naive' datetime
        # We now check the difference is equivalent to the offset we provided
        assert (time_now - dt).seconds == 7200

    def test_get_time_start_success_t1(self):
        """
        Tests get_time_start will return a datetime object and the time start
        """
        time_start = self.tz_time.get_time_start(utc=False, unix=False)
        assert isinstance(time_start, datetime) and \
            self.tz_time.time_start == time_start

    def test_get_time_start_success_t2(self):
        """
        Tests if get_time_start will return a datetime in unix format
        """
        assert self.tz_time.get_time_start(utc=False, unix=True) == 1578780000.0

    def test_get_time_start_success_t3(self):
        """
        Tests if get_time_start will return a datetime in utc time
        """
        time_start = self.tz_time.get_time_start(utc=True, unix=False)
        assert str(time_start.tzinfo) == "UTC"

    def test_get_time_start_success_t4(self):
        """
        Tests if get_time_start will still return unix epoch in UTC if both
        utc and unix arguments are True.
        """
        assert self.tz_time.get_time_start(utc=True, unix=True) == 1578780000.0
