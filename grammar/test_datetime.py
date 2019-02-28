#!/usr/bin/env python3

import unittest
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
from timezonefinder import TimezoneFinder
from datetime import datetime, date, time
import pytz
#deprecated - does not work for some lat/longs# from tzwhere import tzwhere
#deprecated - does not work for some lat/longs# tzw = tzwhere.tzwhere()  # this line is VERY expensive: >4 sec runtime!!
tf = TimezoneFinder()

def is_naive(dt):
    return dt.tzinfo is None

def is_aware(dt):
    return dt.tzinfo is not None

class TestTimeStuff(unittest.TestCase):

    def test_string_to_date_conversion_without_timezone(self):
        date_format = "%d/%m/%y"
        time_format = "%H%M"
        dt = datetime.strptime("13/04/19", date_format)
        self.assertTrue(is_naive(dt))
        print("%s: %s" % (type(dt), str(dt)))
        d = dt.date()
        # self.assertTrue(is_naive(d))
        print("%s: %s" % (type(d), str(d)))
        #not supported# d = date.strptime("13/04/19", date_format)
        #not supported# print(d)
        #not supported#t = time.strptime("1000", time_format)
        #not supported#print(t)
        dt = datetime.strptime("1000", time_format)
        print("%s: %s" % (type(dt), str(dt)))
        t = dt.time()
        self.assertTrue(is_naive(t))
        print("%s: %s" % (type(t), str(t)))

    def test_string_to_date_conversion_with_timezone(self):
        date_format = "%d/%m/%y"
        time_format = "%H%M"
        tz_name = "Europe/Madrid"
        tz_spain = pytz.timezone(tz_name)

# strptime() does not take a tz argument
#        dt = datetime.strptime("13/04/19", date_format, tz=timezone)
#        print("%s: %s" % (type(dt), str(dt)))
#        d = dt.date()
#        print("%s: %s" % (type(d), str(d)))

# we can specify a timezone name but the return date is still naive
        dt = datetime.strptime("13/04/19 1000 AEST", "%d/%m/%y %H%M %Z")
        self.assertTrue(is_naive(dt), "A valid timezone was specfied, tzinfo is still None")
        print("%s: %s" % (type(dt), dt.isoformat()))
        d = dt.date()
        print("%s: %s" % (type(d), dt.isoformat()))
        

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

if __name__ == '__main__':
    unittest.main()
