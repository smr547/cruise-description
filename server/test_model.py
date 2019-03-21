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


class TestAccount(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.dao = AccountDao(Path("./test_content"))

    def test_illegal_operation(self):
        try:
            x = self.dao.find_all()
        except IllegalOperation as e:
            return
        except Exception as e:
            self.fail("Failed to raise IllegalOperation on 'find_all', raised {} instead".format(type(e)))

        self.fail("Failed to raise IllegalOperation on 'find_all'")

    def test_create(self):

        # Note -- don't use the Account constructor directly. Use the AccountDao instead
        trilogy = self.dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.dao.create(trilogy)
        x = self.dao.retrieve(1)
        self.assertEqual(type(x.identifier), type(trilogy.identifier))
        self.assertEqual(x.identifier, trilogy.identifier)
        self.assertEqual(x.name, trilogy.name)
        self.assertEqual(x.email, trilogy.email)
        self.assertEqual(self.dao.next_sequential_id(), 2)

    def test_create_bad_data(self):

        # Account identifier must be numeric
        try:
            trilogy = self.dao.load({'identifier':'abc', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        except ValidationError as e:
            return
        self.fail("Should have got a validation error - non-integer identifier")

class TestVessel(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        self.vessel_dao = VesselDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.account_dao.create(trilogy)

    def test_create(self):
        # Note -- don't use the Account constructor directly. Use the AccountDao instead
        trilogy = self.vessel_dao.load({
            'account_id':1, 
            'identifier':'trilogy', 
            'name':'SV Trilogy', 
            'flag':'Australian',
            'rego':'806176',
            'speed_kts':7.6,
            })
        self.vessel_dao.create(trilogy)
        x = self.vessel_dao.retrieve(1, 'trilogy')
        self.assertEqual(type(x.identifier), type(trilogy.identifier))
        self.assertEqual(x.identifier, trilogy.identifier)
        self.assertEqual(x.name, trilogy.name)
        self.assertEqual(x.flag, trilogy.flag)
        self.assertEqual(x.rego, trilogy.rego)
        self.assertEqual(x.speed_kts, trilogy.speed_kts)

class TestRegion(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.account_dao.create(trilogy)
        self.region_dao = RegionDao(Path("./test_content"), trilogy.identifier)

    def test_create(self):
        # Note -- don't use the Account constructor directly. Use the AccountDao instead
        italy = self.region_dao.load({
            'account_id':1, 
            'region_id':'Italy', 
            'description':'Locations in Italy', 
            'polygon':'Not implemented'
            })
        self.region_dao.create(italy)
        x = self.region_dao.retrieve('Italy')
        self.assertEqual(type(x.region_id), type(italy.region_id))
        self.assertEqual(x.region_id, italy.region_id)
        self.assertEqual(x.account_id, italy.account_id)
        self.assertEqual(x.description, italy.description)
        self.assertEqual(x.polygon, italy.polygon)

class TestLocation(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        trilogy_acc = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.account_dao.create(trilogy_acc)
        self.region_dao = RegionDao(Path("./test_content"), trilogy_acc.identifier)

        italy = self.region_dao.load({
            'account_id':1, 
            'region_id':'italy', 
            'description':'Locations in Italy', 
            'polygon':'Not implemented'
            })
        self.region_dao.create(italy)


    def test_create(self):
        location_dao = LocationDao("./test_content", 1, 'italy')
        rome = location_dao.load({
            'account_id':1, 
            'region_id':'italy', 
            'identifier':'Rome', 
            'name':'Rome, Italy', 
            'coords' : {'longitude': 20.0, 'latitude': 40.0, 'altitude': 200.0},
            'timezone_name':'Europe/Rome'
            })
        location_dao.create(rome)
            
        x = location_dao.retrieve('Rome' )
        self.assertEqual(type(x.region_id), type(rome.region_id))
        self.assertEqual(x.region_id, rome.region_id)
        self.assertEqual(x.account_id, rome.account_id)
        self.assertEqual(x.name, rome.name)

        # can't create twice

        try:
            location_dao.create(rome)
        except ValueError as e:
            return
        self.fail("Should have got a duplication ValueError")

    def test_geocode(self):
        location_dao = LocationDao("./test_content", 1, 'italy')
        rome = Location(1, 'italy', 'Rome', 'Rome, Italy')
        print(rome)
        location_dao.create(rome)
        x = location_dao.retrieve('Rome' )
        print(x)
        self.assertEqual(type(x.region_id), type(rome.region_id))
        self.assertEqual(x.region_id, rome.region_id)
        self.assertEqual(x.account_id, rome.account_id)
        self.assertEqual(x.name, rome.name)
        self.assertEqual(x.timezone_name, rome.timezone_name)
        self.assertEqual(x.coords, rome.coords)




class TestPlan(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        self.vessel_dao = VesselDao(Path("./test_content"))
        account = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
        self.account_dao.create(account)
        trilogy = self.vessel_dao.load({
            'account_id':1, 
            'identifier':'trilogy', 
            'name':'SV Trilogy', 
            'flag':'Australian',
            'rego':'806176',
            'speed_kts':7.6,
            })
        self.vessel_dao.create(trilogy)
        x = self.vessel_dao.retrieve(1, 'trilogy')
        self.plan_dao = PlanDao(Path("./test_content"), account.identifier, trilogy.identifier)

    def test_create(self):
        # Note -- don't use the Account constructor directly. Use the AccountDao instead
        plan = self.plan_dao.load({
            'account_id':1, 
            'vessel_id':'trilogy', 
            'season_id': 'med_summer_2019',
            'plan_id': self.plan_dao.get_random_id(), 
            'cdl':"This is cruise description language\nit breaks over multiple lines"
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
        self.person_dao = PersonDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
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
        x = self.person_dao.retrieve(1, 'fas')
        self.assertEqual(type(x.identifier), type(fred.identifier))
        self.assertEqual(x.identifier, fred.identifier)

class TestSeason(unittest.TestCase):

    def setUp(self):
        os.system("rm -rf ./test_content/*")
        self.account_dao = AccountDao(Path("./test_content"))
        self.vessel_dao = VesselDao(Path("./test_content"))
        self.season_dao = SeasonDao(Path("./test_content"))
        trilogy = self.account_dao.load({'identifier':'1', 'name':'Trilogy Partners', 'email':'svtrilogy@gmail.com'})
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
        x = self.vessel_dao.retrieve(1, 'trilogy')

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
