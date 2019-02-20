#!/usr/bin/env python3

import unittest
from CdlFileAnalyser import CdlFileAnalyser


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
                for e in c.events:
                    print("      -> %s" % (str(e), ))

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
