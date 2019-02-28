#!/usr/bin/env python3

import unittest
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from timezonefinder import TimezoneFinder
from datetime import datetime, date, time, timedelta
import pytz
#deprecated - does not work for some lat/longs# from tzwhere import tzwhere
#deprecated - does not work for some lat/longs# tzw = tzwhere.tzwhere()  # this line is VERY expensive: >4 sec runtime!!
tf = TimezoneFinder()

def is_naive(dt):
    return dt.tzinfo is None

def is_aware(dt):
    return dt.tzinfo is not None

date_format = "%d/%m/%y"
time_format = "%H%M"
tz_name = "Europe/Madrid"
tz_spain = pytz.timezone(tz_name)
tz_athens = pytz.timezone("Europe/Athens")


class TestTimeStuff(unittest.TestCase):

    def test_string_to_date_conversion_without_timezone(self):
        dt = datetime.strptime("13/04/19", date_format)
        self.assertTrue(is_naive(dt))
        self.assertEqual(str(dt), "2019-04-13 00:00:00")

        d = dt.date()
        self.assertEqual(str(d), "2019-04-13")

        dt = datetime.strptime("1000", time_format)
        self.assertEqual(str(dt), "1900-01-01 10:00:00")

        t = dt.time()
        self.assertTrue(is_naive(t))
        self.assertEqual(str(t), "10:00:00")

    def test_string_to_date_conversion_with_timezone(self):

        # we can specify a timezone name but the return date is still naive
        dt = datetime.strptime("13/04/19 1000 AEST", "%d/%m/%y %H%M %Z")
        self.assertTrue(is_naive(dt), "A valid timezone was specfied, tzinfo is still None")
        self.assertEqual(dt.isoformat(), "2019-04-13T10:00:00")

        dt = datetime.strptime("13/04/19 1000 AEST", "%d/%m/%y %H%M %Z")
        dt = tz_spain.localize(dt)
        self.assertTrue(is_aware(dt))
        print("%s: %s" % (type(dt), dt.isoformat()))
        d = dt.date()
        print("%s: %s" % (type(d), dt.isoformat()))

        # construct an "aware" datetime
        dt = datetime.strptime("13/04/19", date_format)
        dt = tz_spain.localize(dt)
        t = datetime.strptime("1000", time_format)
        t = t.time()
        dt = datetime.combine(dt, t)
        self.assertTrue(is_naive(dt))
        dt = tz_spain.localize(dt)
        self.assertTrue(is_aware(dt))
        print("%s: %s" % (type(dt), dt.isoformat()))
        d = dt.date()
        print("%s: %s" % (type(d), dt.isoformat()))

        dt = datetime.strptime("1000", time_format)
        print("%s: %s" % (type(dt), str(dt)))
        t = dt.time()
        print("%s: %s" % (type(t), str(t)))
        

    def test_find_tz_with_lat_long(self):
        pass
#deprecated - does not work for some lat/longs#         timezone_str = tzw.tzNameAt(37.3880961, -5.9823299) # Seville coordinates
        # self.assertEqual(timezone_str, "Europe/Madrid")
        # timezone = pytz.timezone(timezone_str)
        dt = datetime.now()
        print(dt)
        print(dt.isoformat())
        # print(timezone.utcoffset(dt))
        # dt = datetime.now(timezone)
        # print(dt)
        # print(dt.isoformat())


    def test_awareness_survival(self):
        dt = datetime.strptime("13/04/19", date_format)
        dt = tz_spain.localize(dt)
        t = datetime.strptime("1000", time_format)
        t = t.time()
        dt = datetime.combine(dt, t)
        self.assertTrue(is_naive(dt))

        # advance two days

        td = timedelta(days=2) 
        new_dt = dt + td
        self.assertEqual(new_dt.isoformat(), "2019-04-15T10:00:00")
        self.assertTrue(is_naive(new_dt), "after date/time arithmetic, the result is naive")
        new_dt = tz_spain.localize(new_dt)
        self.assertTrue(is_aware(new_dt), "once localized the datetime is aware")
        self.assertEqual(new_dt.isoformat(), "2019-04-15T10:00:00+02:00")

        # change time zone
        dt = new_dt.astimezone(tz_athens)
        self.assertEqual(dt.isoformat(), "2019-04-15T11:00:00+03:00")


        

if __name__ == '__main__':
    unittest.main()
