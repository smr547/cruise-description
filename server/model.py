#!/usr/bin/env python3
import datetime as dt
from random import randint
from marshmallow import Schema, fields, pprint, post_load
from pathlib import Path


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
        return self.schema()

    def load(self, aDict):
        schema = self.get_schema()
        return schema.load(aDict)

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
    def __init__(self, content_base):
        self.schema = VesselSchema
        self.content_base = content_base

    def _get_json_path(self, account_id, vessel_id):
        return Path("{}/accounts/{}/vessels/{}/vessel.json".format(self.content_base, 
            account_id, vessel_id))

    def create(self, vessel):
        vessel_dir = self._get_json_path(vessel.account_id, vessel.identifier ).parent
        if vessel_dir.exists():
            raise ValueError("{} exists on Vessel creation".format(str(vessel.identifier)))
        vessel_dir.mkdir(parents=True)
        self.save(vessel)

    def save(self, vessel):
        json_path = self._get_json_path(vessel.account_id, vessel.identifier)
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(vessel, indent=2))
    
    def retrieve(self, account_id, vessel_id):
        json_path = self._get_json_path(account_id, vessel_id)
        if not json_path.exists():
            raise ValueError("Vessel {} doesn't exist in account {}".format(vessel_id, account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

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
    def __init__(self, content_base, account_id, vessel_id):
        self.schema = PlanSchema
        self.content_base = content_base
        self.account_id = account_id
        self.vessel_id = vessel_id
    
    def _check_context(self, plan):
        if (self.account_id != plan.account_id) or \
           (self.vessel_id != plan.vessel_id):
           raise IllegalOperatin("Plan does not match DAO context")

    def get_random_id(self, width=4):
        chars = 'abcdefghjklmnpqrstuvwxyz'.upper()
        while True:
            plan_id = ""
            for i in range(0,width):
                j = randint(0, len(chars)-1)
                plan_id += chars[j]
            if not self._get_json_path(plan_id).exists():
                return plan_id

        
    def _get_json_path(self, plan_id):
        return Path("{}/accounts/{}/vessels/{}/plans/{}.json".format(self.content_base, 
            self.account_id, self.vessel_id, plan_id))

    def create(self, plan):
        self._check_context(plan)
        plan_file = self._get_json_path(plan.plan_id)
        if plan_file.exists():
            raise ValueError("Plan {} already exists".format(str(plan.plan_id)))
        if not plan_file.parent.exists():
            plan_file.parent.mkdir(parents=True)
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
            raise ValueError("Plan {} doesn't exist in account {} for vessel {}".format(plan_id, 
                self.account_id, self.vessel_id))
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
    def __init__(self, content_base):
        self.schema = PersonSchema
        self.content_base = content_base

    def _get_json_path(self, account_id, person_id):
        return Path("{}/accounts/{}/persons/{}.json".format(self.content_base, 
            account_id, person_id))

    def create(self, person):
        person_path = self._get_json_path(person.account_id, person.identifier )
        if person_path.exists():
            raise ValueError("Person file for {} already exists".format(str(person.identifier)))
        person_path.parent.mkdir(parents=True)
        self.save(person)

    def save(self, person):
        json_path = self._get_json_path(person.account_id, person.identifier )
        with open(json_path, 'w') as outfile:
            schema = self.get_schema()
            outfile.write(schema.dumps(person, indent=2))
    
    def retrieve(self, account_id, person_id):
        json_path = self._get_json_path(account_id, person_id)
        if not json_path.exists():
            raise ValueError("Person {} doesn't exist in account {}".format(person_id, account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = self.get_schema()
            return schema.loads(infile.read())

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
