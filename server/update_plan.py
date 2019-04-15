#!/usr/bin/env python3

from pathlib import Path
import unittest
from model import IllegalOperation,  \
    Account, AccountDao,  \
    Vessel, VesselDao, \
    Person, PersonDao, \
    Plan, PlanDao, \
    Region, RegionDao, \
    Location, LocationDao, \
    Season, SeasonDao

from marshmallow.exceptions import ValidationError
import os

class TestPlan(unittest.TestCase):

    def test_create_with_cdl(self):
        with open("../grammar/plan_B.cdl", 'r') as infile:
            cdl = infile.read()
        plan = self.plan_dao.load({
            'account_id':1, 
            'vessel_id':'trilogy', 
            'season_id': 'med_summer_2019',
            'plan_id': self.plan_dao.get_random_id(), 
            'cdl': cdl
            })
        self.plan_dao.create(plan)
        x = self.plan_dao.retrieve(plan.plan_id)
        self.assertEqual(type(x.plan_id), type(plan.plan_id))
        self.assertEqual(x.plan_id, plan.plan_id)
        self.assertEqual(x.account_id, plan.account_id)
        self.assertEqual(x.vessel_id, plan.vessel_id)
        self.assertEqual(x.season_id, plan.season_id)
        self.assertEqual(x.cdl, plan.cdl)

class TestPerson(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':1, 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.person_dao = PersonDao(Path("./test_content"), trilogy.identifier)
        self.account_dao.create(trilogy)

    def test_create(self):
        fred = self.person_dao.load({
            'account_id':1, 
            'identifier':"fas",
            'surname':'Smith',
            'first_names':'Frederick Alexander',
            'address':'17 Constitution Ave, Canberra, ACT 2612',
            'email': 'fred.smith@gmail.com',
            'phone': '+61234567273',
            'gender': 'MALE',
            'passport_no': 'P1234543212',
            'passport_country': 'Australia',
            'passport_issued': '2012-10-25',
            'passport_expiry': '2022-10-25',
            'skills': "",
            'blood_group': 'O+ve',
            'allergies': '',
            'medication': '',
            'quals': 'Yachtmaster, senior first aid'
      #      'nok_id=None,
      #      'nok_relationship=None,
      #      'next_flight_in=None,
      #      'next_flight_out=None,
            })
        self.person_dao.create(fred)
        x = self.person_dao.retrieve('fas')
        self.assertEqual(type(x.identifier), type(fred.identifier))
        self.assertEqual(x.identifier, fred.identifier)

class TestSeason(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':1, 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.vessel_dao = VesselDao(Path("./test_content"), trilogy.identifier)
        self.season_dao = SeasonDao(Path("./test_content"))
        self.account_dao.create(trilogy)
        trilogy = self.vessel_dao.load({
            'account_id':1, 
            'identifier':'trilogy', 
            'name':'SV Trilogy', 
            'flag':'Australian',
            'rego':'806176',
            'speed_kts':7.6,
            })
        self.vessel_dao.create(trilogy)
        x = self.vessel_dao.retrieve('trilogy')

    def test_create(self):
        season = self.season_dao.load({
            'account_id':1, 
            'identifier':'med_summer_2019', 
            'name':'Mediterranean 2019' 
            })
        self.season_dao.create(season)
        x = self.season_dao.retrieve(1, 'med_summer_2019')
        self.assertEqual(type(x.identifier), type(season.identifier))
        self.assertEqual(x.identifier, season.identifier)
        self.assertEqual(x.name, season.name)


if __name__ == '__main__':
    unittest.main()
