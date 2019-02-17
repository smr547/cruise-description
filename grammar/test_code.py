#!/usr/bin/env python3

import unittest
from CdlFileAnalyser import CdlFileAnalyser


class TestCdlAnalyser(unittest.TestCase):

    def test_analyser_instantiation(self):
        analyser = CdlFileAnalyser()
        self.assertTrue(analyser is not None)

    def test_analysis(self):
        filename = './test_cruise.cdl'
        analyser = CdlFileAnalyser()
        content = analyser.analyse(filename)
        self.assertTrue(content is not None)

    def test_analysis_returned_content(self):
        filename = './test_cruise.cdl'
        analyser = CdlFileAnalyser()
        content = analyser.analyse(filename)
        seasons = content.vesselSeasons
        self.assertEqual(len(seasons), 1)

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
