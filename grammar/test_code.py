#!/usr/bin/env python3

import unittest
from CdlFileAnalyser import CdlFileAnalyser
from scheduler import schedule_season
# from timezonefinder import TimezoneFinder
# from datetime import datetime, date, time
# import pytz
#deprecated - does not work for some lat/longs# from tzwhere import tzwhere
#deprecated - does not work for some lat/longs# tzw = tzwhere.tzwhere()  # this line is VERY expensive: >4 sec runtime!!
# tf = TimezoneFinder()

class TestScheduler(unittest.TestCase):

    def setUp(self):
        filename = './test_cruise.cdl'
        analyser = CdlFileAnalyser()
        self.content = analyser.analyse(filename)

    def test_cruise_departures(self):
        for vs in self.content.vesselSeasons.values():
            for c in vs.cruises:
                print("Cruise %s departs from %s at %s" % (c.name, c.departure_port.identifier, 
                    c.get_departure_dt().isoformat()))

    def test_scheduler(self):
        for vs in self.content.vesselSeasons.values():
          schedule_season(vs)

#   def test_timezones(self):
#       for loc in self.content.locations.values():
#           timezone_str = tzw.tzNameAt(loc.lat(), loc.lng())
#           print("%s : %s at (%f,%f)" % (loc.identifier, timezone_str, loc.lat(), loc.lng()))
#           pass

    def test_timezones_tf(self):
        for loc in self.content.locations.values():
            timezone_str = loc.timezone_name()
            tz = loc.get_timezone()
            # timezone_str = tf.timezone_at(lng=loc.lng(), lat=loc.lat())
            print("%s : %s at (%f,%f)" % (loc.identifier, timezone_str, loc.lat(), loc.lng()), str(tz))

class TestCdlAnalyser(unittest.TestCase):

    def setUp(self):
        filename = './test_cruise.cdl'
        analyser = CdlFileAnalyser()
        self.content = analyser.analyse(filename)


    def test_analysis(self):
        content = self.content
        self.assertTrue(content is not None)

    def test_analysis_returned_content(self):
        content = self.content
        seasons = content.vesselSeasons
        self.assertEqual(len(seasons), 1)
        for s in seasons.values():
            print(s.identifier())
            for c in s.cruises:
                print("   %s" % (str(c), ))
                for l in c.legs:
                    print("      -> %s" % (str(l), ))
                for l in c.events:
                    print("      -> %s" % (str(l), ))

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
