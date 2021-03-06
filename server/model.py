#!/usr/bin/env python3

from math import isclose
import datetime as dt
from random import randint
from marshmallow import Schema, fields, pprint, post_load
from pathlib import Path
from timezonefinder import TimezoneFinder
import pytz
from geolocator import CachedGeoLocator
from geopy.distance import great_circle



class IllegalOperation(Exception):
    pass

class Dao(object):
    def create(self, identifier):
        raise IllegalOperation("'create' not permitted on {} object".format(type(self)))

    def save(self, instance):
        raise IllegalOperation("'save' not permitted on {} object".format(type(self)))

    def retrieve(self, identifier):
        raise IllegalOperation("'retrieve' not permitted on {} object".format(type(self)))

    def find_all(self):
        raise IllegalOperation("'find_all' not permitted on {} object".format(type(self)))

    def next_sequential_id(self):
        raise IllegalOperation("'next_sequential_id' not permitted on {} object".format(type(self)))

    def get_schema(self):
        '''
        Return an instance of the Schema for the Entity related to this Data Access Object
        '''
        return self.schema()

    def load(self, aDict):
        schema = self.get_schema()
        return schema.load(aDict)

    def from_json(self, json_string):
        schema = self.get_schema()
        return schema.loads(json_string)

#############################################################
###                                                       ###
###                 ACCOUNT                               ###
###                                                       ###
#############################################################

class AccountSchema(Schema):

    class Meta:
        ordered = True

    identifier = fields.Integer(required=True)
    name = fields.Str(required=True)
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_account(self, data):
        return Account(**data)

class Account(object):
    def __init__(self, identifier, name, email, created_at=None):
        self.identifier = identifier
        self.name = name
        self.email = email
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Account(name={self.name!r})>'.format(self=self)

class AccountDao(Dao):
    def __init__(self, content_base):
        self.schema = AccountSchema
        self.content_base = content_base

    def next_sequential_id(self):
        '''
        Returns the next available account identifier
        '''
        account_dir = self._get_json_path(0).parent.parent
        m = 0
        for p in account_dir.iterdir():
            m = max(m, int(p.name))
        return m+1

    def _get_json_path(self, account_id):
        return Path("{}/accounts/{}/account.json".format(self.content_base, account_id))

    def create(self, account):
        account_dir = self._get_json_path(account.identifier).parent
        if account_dir.exists():
            raise ValueError("{} exists on Account creation".format(str(account_dir)))
        account_dir.mkdir(parents=True)
        account_dir.joinpath("persons").mkdir()
        account_dir.joinpath("vessels").mkdir()
        account_dir.joinpath("seasons").mkdir()
        account_dir.joinpath("plans").mkdir()
        account_dir.joinpath("regions").mkdir()
        account_dir.joinpath("locations").mkdir()
        self.save(account)

    def save(self, account):
        json_path = self._get_json_path(account.identifier)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(account, indent=2))
    
    def retrieve(self, account_id):
        json_path = self._get_json_path(account_id)
        if not json_path.exists():
            raise ValueError("Account {} doesn't exist".format(account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

#############################################################
###                                                       ###
###                 VESSEL                                ###
###                                                       ###
#############################################################

class VesselSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    identifier = fields.String(required=True)
    name = fields.Str(required=True)
    flag = fields.Str(required=True)
    rego = fields.Str(required=True)
    speed_kts = fields.Float(required=True)
    created_at = fields.DateTime()

    @post_load
    def make_vessel(self, data):
        return Vessel(**data)

class Vessel(object):
    def __init__(self, account_id, identifier, name, flag, rego, speed_kts, created_at=None):
        self.account_id = account_id
        self.identifier = identifier
        self.name = name
        self.flag = flag
        self.rego = rego
        self.speed_kts = speed_kts
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Vessel(name={self.name!r})>'.format(self=self)

class VesselDao(Dao):
    def __init__(self, content_base, account_id):
        self.schema = VesselSchema
        self.content_base = content_base
        self.account_id = account_id
    
    def _check_context(self, vessel):
        if (self.account_id != vessel.account_id):
           raise IllegalOperation("Account id for vessel ({}) does not match DAO context (Account id={})".\
               format(vessel.account_id, self.account_id))

    def _get_json_path(self, vessel_id=None):
        dir_path = Path("{}/accounts/{}/vessels".format(self.content_base, self.account_id))
        if vessel_id is None:
            return dir_path
        return dir_path.joinpath("{}/vessel.json".format(vessel_id))

    def create(self, vessel):
        self._check_context(vessel)
        vessel_dir = self._get_json_path(vessel.identifier).parent
        if vessel_dir.exists():
            raise ValueError("{} exists on Vessel creation".format(str(vessel.identifier)))
        vessel_dir.mkdir(parents=True)
        self.save(vessel)

    def save(self, vessel):
        self._check_context(vessel)
        json_path = self._get_json_path(vessel.identifier)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(vessel, indent=2))
    
    def retrieve(self, vessel_id):
        json_path = self._get_json_path(vessel_id)
        if not json_path.exists():
            raise ValueError("Vessel {} doesn't exist in account {}".format(vessel_id, self.account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

    def find_all(self):
        return [self.retrieve(p.name) for p in self._get_json_path().iterdir()]
        
        


#############################################################
###                                                       ###
###                 SEASON                                ###
###                                                       ###
#############################################################

class SeasonSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    identifier = fields.String(required=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime()

    @post_load
    def make_season(self, data):
        return Season(**data)

class Season(object):
    def __init__(self, account_id, identifier, name, created_at=None):
        self.account_id = account_id
        self.identifier = identifier
        self.name = name
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Season(name={self.name!r})>'.format(self=self)

class SeasonDao(Dao):
    def __init__(self, content_base):
        self.schema = SeasonSchema
        self.content_base = content_base

    def _get_json_path(self, account_id, season_id):
        return Path("{}/accounts/{}/seasons/{}/season.json".format(self.content_base, 
            account_id, season_id))

    def create(self, season):
        season_dir = self._get_json_path(season.account_id, season.identifier ).parent
        if season_dir.exists():
            raise ValueError("{} exists on Season creation".format(str(season.identifier)))
        season_dir.mkdir(parents=True)
        self.save(season)

    def save(self, season):
        json_path = self._get_json_path(season.account_id, season.identifier)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(season, indent=2))
    
    def retrieve(self, account_id, season_id):
        json_path = self._get_json_path(account_id, season_id)
        if not json_path.exists():
            raise ValueError("Season {} doesn't exist in account {}".format(season_id, account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

#############################################################
###                                                       ###
###                 PLAN                                  ###
###                                                       ###
#############################################################

class PlanSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    vessel_id = fields.String(required=True)
    season_id = fields.String(required=True)
    plan_id = fields.String(required=True)
    cdl = fields.Str(required=True)
    created_at = fields.DateTime()

    @post_load
    def make_plan(self, data):
        return Plan(**data)

class Plan(object):
    def __init__(self, account_id, vessel_id, season_id, plan_id,  cdl, created_at=None):
        self.account_id = account_id
        self.vessel_id = vessel_id
        self.season_id = season_id
        self.plan_id = plan_id
        self.cdl = cdl
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Plan(plan_id={self.plan_id!r})>'.format(self=self)

class PlanDao(Dao):
    def __init__(self, content_base, account_id):
        self.schema = PlanSchema
        self.content_base = content_base
        self.account_id = account_id
    
    def _check_context(self, plan):
        if (self.account_id != plan.account_id): 
           raise IllegalOperations("Plan does not match DAO context")

    def get_random_id(self, width=4):
        chars = 'abcdefghjklmnpqrstuvwxyz'.upper()
        while True:
            plan_id = ""
            for i in range(0,width):
                j = randint(0, len(chars)-1)
                plan_id += chars[j]
            if not self._get_json_path(plan_id).exists():
                return plan_id

    def _get_json_path(self, plan_id=None):
        dir_path = Path("{}/accounts/{}/plans".format(self.content_base, self.account_id))
        if plan_id is None:
            return dir_path
        return dir_path.joinpath("{}.json".format(plan_id))
        
    def create(self, plan):
        self._check_context(plan)
        plan.plan_id = self.get_random_id()
        plan_file = self._get_json_path(plan.plan_id)
        if plan_file.exists():
            raise ValueError("Plan {} already exists".format(str(plan.plan_id)))
        self.save(plan)

    def save(self, plan):
        self._check_context(plan)
        json_path = self._get_json_path(plan.plan_id)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(plan, indent=2))
    
    def retrieve(self, plan_id):
        json_path = self._get_json_path(plan_id)
        if not json_path.exists():
            raise ValueError("Plan {} doesn't exist in account {}".format(plan_id, 
                self.account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

    def find_all(self):
        return [self.retrieve(p.stem) for p in self._get_json_path().iterdir()]

#############################################################
###                                                       ###
###                 REGION                                ###
###                                                       ###
#############################################################

class RegionSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    region_id = fields.String(required=True)
    description = fields.String(required=False)
    polygon = fields.String(required=False)
    created_at = fields.DateTime()

    @post_load
    def make_region(self, data):
        return Region(**data)

class Region(object):
    def __init__(self, account_id, region_id, description, polygon="Not implemented", created_at=None):
        self.account_id = account_id
        self.region_id = region_id
        self.description = description
        self.polygon = polygon
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Region(reegion_id={self.region_id!r})>'.format(self=self)

class RegionDao(Dao):
    def __init__(self, content_base, account_id):
        self.schema = RegionSchema
        self.content_base = content_base
        self.account_id = account_id
    
    def _check_context(self, region):
        if (self.account_id != region.account_id):
           raise IllegalOperations("Region does not match DAO context")

    def _get_json_path(self, region_id):
        return Path("{}/accounts/{}/regions/{}/region.json".format(self.content_base, 
            self.account_id, region_id))

    def create(self, region):
        self._check_context(region)
        region_file = self._get_json_path(region.region_id)
        if region_file.exists():
            raise ValueError("Regions {} already exists".format(str(region.region_id)))
        if not region_file.parent.exists():
            region_file.parent.mkdir(parents=True)
        self.save(region)

    def save(self, region):
        self._check_context(region)
        json_path = self._get_json_path(region.region_id)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(region, indent=2))
    
    def retrieve(self, region_id):
        json_path = self._get_json_path(region_id)
        if not json_path.exists():
            raise ValueError("Region {} doesn't exist in account {}".format(region_id, 
                self.account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

#############################################################
###                                                       ###
###         COORDS and LOCATION                           ###
###                                                       ###
#############################################################

class CoordsSchema(Schema):
    class Meta:
        ordered = True

    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)
    altitude = fields.Float(required=False)

    @post_load
    def make_coords(self, data):
        return Coords(**data)
    

class Coords(object):
    def __init__(self, longitude, latitude, altitude=0.0):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude

    def __repr__(self):
        return '<Coords(long={self.longitude}, lat={self.latitude})>'.format(self=self)

    def __eq__(self, rhs):
        return isclose(self.longitude, rhs.longitude, rel_tol=1e-7) and \
               isclose(self.latitude, rhs.latitude, rel_tol=1e-7) and \
               isclose(self.altitude, rhs.altitude, rel_tol=1e-7)

class LocationSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    region_id = fields.String(required=True)
    identifier = fields.String(requred=True)
    name = fields.Str(required=True)
    coords = fields.Nested(CoordsSchema, required=False)
    timezone_name = fields.String(required=False)
    created_at = fields.DateTime()

    @post_load
    def make_location(self, data):
        return Location(**data)

class Location(object):
    
    _locator = CachedGeoLocator().load()
    _tf = TimezoneFinder()

    @classmethod
    def save_cache(cls):
        if cls._locator is not None:
            cls._locator.save()

    def __init__(self, account_id, region_id, identifier, name, coords=None, timezone_name=None, created_at=None):
        self.account_id = account_id
        self.region_id = region_id
        self.identifier = identifier
        self.name = name
        self.coords = coords
        self.timezone_name = timezone_name
        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

        if self.coords is None:
            # Use geolocation service to determine coords based on name of location
            loc = self._locator.get_location(name)
            self.coords = Coords(loc['lng'],  loc['lat'])
            self.timezone_name = None

        if self.timezone_name is None:
            self.timezone_name = self._tf.timezone_at(lng=self.lng(), lat=self.lat())

    def lat(self):
        return self.coords.latitude

    def lng(self):
        return self.coords.longitude

    def alt(self):
        return self.coords.altitude

    def asLatLongTuple(self):
        return (coords.latitude, coords.longitude)

    def get_timezone(self):
        return pytz.timezone(self.timezone_name)

    def distance_NM(self, to_location):
        return great_circle(self.asLatLongTuple(), self.to_location.asLatLongTuple()).miles

    def __repr__(self):
        return '<Location(region={self.region_id}, id={self.identifier}, name={self.name!r}, coords={self.coords}, tz={self.timezone_name})>'.format(self=self)

class LocationDao(Dao):
    def __init__(self, content_base, account_id, region_id):
        self.schema = LocationSchema
        self.content_base = content_base
        self.account_id = account_id
        self.region_id = region_id

        # check region exists
        region = RegionDao(content_base, account_id).retrieve(region_id)
    
    def _check_context(self, location):
        if (self.account_id != location.account_id) or \
           (self.region_id != location.region_id):
           raise IllegalOperation("Location does not match DAO context")

    def _get_json_path(self, identifier):
        return Path("{}/accounts/{}/locations/{}/{}.json".format(self.content_base, 
            self.account_id, self.region_id, identifier))

    def create(self, location : Location):
        self._check_context(location)
        json_path = self._get_json_path(location.identifier)
        if json_path.exists():
            raise ValueError("{} exists on Location creation".format(str(location.identifier)))
        region_dir = json_path.parent
        if not region_dir.exists():
            region_dir.mkdir(parents=True)
        self.save(location)

    def save(self, location : Location):
        self._check_context(location)
        json_path = self._get_json_path(location.identifier)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(location, indent=2))
    
    def retrieve(self, identifier):
        json_path = self._get_json_path(identifier)
        if not json_path.exists():
            raise ValueError("Location {} doesn't exist in account {}".format(identifier, account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())


#############################################################
###                                                       ###
###                 PERSON                                ###
###                                                       ###
#############################################################

class PersonSchema(Schema):

    class Meta:
        ordered = True

    account_id = fields.Integer(required=True)
    identifier = fields.String(required=True)
    surname = fields.Str(required=True)
    first_names = fields.Str(required=True)
    address = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    gender = fields.Str(required=True)
    passport_no = fields.Str(required=False)
    passport_country = fields.Str(required=False)
    passport_issued = fields.Date(required=False)
    passport_expiry = fields.Date(required=False)
    skills = fields.Str(required=False)
    blood_group = fields.Str(required=False)
    allergies = fields.Str(required=False)
    medication = fields.Str(required=False)
    quals = fields.Str(required=False)
    nok_id = fields.Str(required=False)
    nok_relationship = fields.Str(required=False)
    next_flight_in = fields.Str(required=False)
    next_flight_out = fields.Str(required=False)
    created_at = fields.DateTime()

    @post_load
    def make_person(self, data):
        return Person(**data)

class Person(object):
    def __init__(self, 
        account_id,
        identifier,
        surname,
        first_names,
        address,
        email,
        phone,
        gender,
        passport_no='',
        passport_country='',
        passport_issued='',
        passport_expiry='',
        skills='',
        blood_group='',
        allergies='',
        medication='',
        quals='',
        nok_id='',
        nok_relationship='',
        next_flight_in='',
        next_flight_out='',
        created_at=None):

        self.account_id = account_id
        self.identifier = identifier
        self.surname = surname
        self.first_names = first_names
        self.address = address
        self.email = email
        self.phone = phone
        self.passport_no = passport_no
        self.passport_country = passport_country
        self.passport_issued = passport_issued
        self.passport_expiry = passport_expiry 
        self.gender = gender
        self.skills = skills
        self.blood_group = blood_group
        self.allergies = allergies
        self.medication = medication
        self.quals = quals
        self.nok_id = nok_id
        self.nok_relationship = nok_relationship
        self.next_flight_in = next_flight_in
        self.next_flight_out = next_flight_out

        if created_at is None:
            self.created_at = dt.datetime.now()
        else:
            self.created_at = created_at

    def __repr__(self):
        return '<Person(id={self.identifier!r})>'.format(self=self)

class PersonDao(Dao):
    def __init__(self, content_base, account_id):
        self.schema = PersonSchema
        self.content_base = content_base
        self.account_id = account_id
    
    def _check_context(self, person):
        if (self.account_id != person.account_id):
           raise IllegalOperation("Account id for Person ({}) does not match DAO context (Account id={})".\
               format(person.account_id, self.account_id))

    def _get_json_path(self, person_id=None):
        dir_path = Path("{}/accounts/{}/persons".format(self.content_base, self.account_id))
        if person_id is None:
            return dir_path
        return dir_path.joinpath("{}.json".format(person_id))

    def create(self, person):
        self._check_context(person)
        person_path = self._get_json_path(person.identifier )
        if person_path.exists():
            raise ValueError("Person '{}' already exists on server".format(str(person.identifier)))
        self.save(person)

    def save(self, person):
        self._check_context(person)
        json_path = self._get_json_path(person.identifier )
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(person, indent=2))

    def delete(self, person_identifier):
        json_path = self._get_json_path(person_identifier)
        if not json_path.exists():
            raise ValueError("Person '{}' does not exist".format(person_identifier))
        json_path.unlink()
    
    def retrieve(self, person_id):
        json_path = self._get_json_path(person_id)
        if not json_path.exists():
            raise ValueError("Person {} doesn't exist in account {}".format(person_id, self.account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

    def find_all(self):
        return [self.retrieve(p.stem) for p in self._get_json_path().iterdir()]

#############################################################


if __name__ == "__main__":
    trilogy = Account(identifier=1, name="Trilogy Partners", email="svtrilogy@gmail.com")
    print(trilogy)
    schema = AccountSchema()
    result = schema.dump(trilogy)
    pprint(result, indent=2)

    


    dao = AccountDao("/Users/stevenring/planacruise/content")

    x = dao.find_all()
    dao.create(trilogy)

    account = dao.retrieve(1)
    print("Retrieved account is {}".format(account))


    # deserialise

    account_data = {
    'identifier': 2,
    'created_at': '2014-08-11T05:26:03.869245',
    'email': u'ken@yahoo.com',
    'name': u'Ken'
    }

    account = schema.load(account_data)
    print(account)
    print(account.created_at)
