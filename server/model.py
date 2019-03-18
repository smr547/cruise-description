#!/usr/bin/env python3
import datetime as dt
from marshmallow import Schema, fields, pprint, post_load
from pathlib import Path

class AccountSchema(Schema):

    class Meta:
        ordered = True

    identifier = fields.Int()
    name = fields.Str()
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


class AccountDao(object):
    def __init__(self, content_base):
        self.content_base = content_base

    def _get_json_path(self, account_id):
        return Path("{}/accounts/{}/account.json".format(self.content_base, account_id))


    def create(self, account):
        account_dir = self._get_json_path(account.identifier).parent
        if account_dir.exists():
            raise ValueError("{} exists on Account creation".format(str(account_dir)))
        account_dir.mkdir()
        self.save(account)

    def save(self, account):
        json_path = self._get_json_path(account.identifier)
        with open(json_path, 'w') as outfile:
            schema = AccountSchema()
            outfile.write(schema.dumps(account, indent=2))
        
    
    def retrieve(self, account_id):
        json_path = self._get_json_path(account_id)
        if not json_path.exists():
            raise ValueError("Account {} doesn't exist".format(account_id))
        with open(json_path, 'r', encoding='utf-8') as infile:
            schema = AccountSchema()
            return schema.loads(infile.read())


if __name__ == "__main__":
    trilogy = Account(identifier=1, name="Trilogy Partners", email="svtrilogy@gmail.com")
    print(trilogy)
    schema = AccountSchema()
    result = schema.dump(trilogy)
    pprint(result, indent=2)


    dao = AccountDao("/Users/stevenring/planacruise/content")
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


