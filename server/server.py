#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify
from pathlib import Path
from model import VesselDao, PersonDao, PlanDao
from io import StringIO

from cdl_preprocessor import preprocess
from CdlFileAnalyser import CdlFileAnalyser
from toKml import cdlfile_to_KML
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

content = Path("./test_content")

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/publish_locations", methods=['POST'])
def publish_locations():
    os.system("./deploy_locations.sh")
    return  "", 200


@app.route("/cruise_kml", methods=['GET'])
def cruise_kml():
    kml = ""
    with open("./test_cruise.kml", 'r') as f_in:
        kml = f_in.read()
   
    return  kml, 200, {'Content-Type': 'application/vnd.google-earth.kml+xml; charset=utf-8'}

@app.route("/locations", methods=['GET'])
def locations():
    path = "%s/locations" % (content, )
    r = ""
    for f in os.listdir(path) :
        if f.endswith(".txt") or f.endswith(".cdl") :
            r += "%s\n" % (f, ) 
   
    return  r, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/locations/<path:subpath>", methods=['GET'])
def locations_file(subpath):
    path = "%s/locations/%s" % (content, subpath)
    try:
        with open(path, 'r') as f_in:
            r = f_in.read()
            if path.endswith(".kml"):
                headers = {'Content-Type': 'application/vnd.google-earth.kml+xml; charset=utf-8'}
            else:
                headers = {'Content-Type': 'text/plain; charset=utf-8'}
            return  r, 200, headers
    except Exception:
        return "", 404

@app.route("/<int:account_id>/vessel/", methods=['GET'])
def vessel_list(account_id):
    dao = VesselDao(content, account_id)
    vessels = dao.find_all()
    return dao.get_schema().dumps(vessels, many=True, indent=2), 200

@app.route("/<int:account_id>/vessel/", methods=['POST'])
def vessel_add(account_id):
    dao = VesselDao(content, account_id)
    vessel = dao.from_json(request.data)
    dao.create(vessel)
    vessel = dao.retrieve(vessel.identifier)
    return dao.get_schema().dumps(vessel, indent=2), 200


@app.route("/<int:account_id>/vessel/<identifier>/", methods=['GET'])
def vessel(account_id, identifier):
    dao = VesselDao(content, account_id)
    vessel = dao.retrieve(identifier)
    return dao.get_schema().dumps(vessel, indent=2), 200

@app.route("/<int:account_id>/person/", methods=['GET'])
@api.representation('application/json')
def person_list(account_id):
    try:
        dao = PersonDao(content, account_id)
        people = dao.find_all()
        return dao.get_schema().dumps(people, many=True, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/person/", methods=['POST'])
def person_create(account_id):
    try:
        dao = PersonDao(content, account_id)
        person = dao.from_json(request.data)
        dao.create(person)
        person = dao.retrieve(person.identifier)
        return dao.get_schema().dumps(person, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/person/<identifier>/", methods=['GET'])
def person_read(account_id, identifier):
    try:
        dao = PersonDao(content, account_id)
        person = dao.retrieve(identifier)
        return dao.get_schema().dumps(person, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/person/<identifier>/", methods=['PUT'])
def person_update(account_id, identifier):
    try:
        dao = PersonDao(content, account_id)
        person = dao.retrieve(identifier)
        new_person = dao.from_json(request.data)
        if new_person.identifier != person.identifier:
            raise ValueError("Cannot change idenitifier from {} to {}".format(person.identifier, new_person.identifier))
        dao.save(new_person)
        return dao.get_schema().dumps(new_person, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/person/<identifier>/", methods=['DELETE'])
def person_delete(account_id, identifier):
    try:
        dao = PersonDao(content, account_id)
        person = dao.retrieve(identifier)
        dao.delete(identifier)
        return dao.get_schema().dumps(person, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/plan/", methods=['GET'])
def plan_list(account_id):
    dao = PlanDao(content, account_id)
    plans = dao.find_all()
    return dao.get_schema().dumps(plans, many=True, indent=2), 200

@app.route("/<int:account_id>/plan/", methods=['POST'])
def plan_add(account_id):
    dao = PlanDao(content, account_id)
    plan = dao.from_json(request.data)
    dao.create(plan)
    plan = dao.retrieve(plan.plan_id)
    return dao.get_schema().dumps(plan, indent=2), 200

@app.route("/<int:account_id>/plan/<plan_id>/", methods=['GET'])
def plan(account_id, plan_id):
    try:
        dao = PlanDao(content, account_id)
        plan = dao.retrieve(plan_id)
        return dao.get_schema().dumps(plan, indent=2), 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/plan/<plan_id>/", methods=['PUT'])
def plan_update(account_id, plan_id):
    try:
        dao = PlanDao(content, account_id)
        plan = dao.retrieve(plan_id)
        plan = dao.from_json(request.data)
        if plan_id !=  plan.plan_id:
            raise Exception("Cannot change the plan ID")
        dao.save(plan)
    except Exception as e:
        raise InvalidUsage(str(e))
    
    return dao.get_schema().dumps(plan, indent=2), 200

@app.route("/<int:account_id>/plan/<plan_id>.cdl/", methods=['GET'])
def get_plan_cdl(account_id, plan_id):
    dao = PlanDao(content, account_id)
    plan = dao.retrieve(plan_id)
    return plan.cdl, 200

@app.route("/<int:account_id>/plan/<plan_id>.cdl/", methods=['PUT'])
def update_plan_cdl(account_id, plan_id):
    try:
        dao = PlanDao(content, account_id)
        plan = dao.retrieve(plan_id)
        plan.cdl = request.data
        dao.save(plan)
        return plan.cdl, 200
    except Exception as e:
        raise InvalidUsage(str(e))

@app.route("/<int:account_id>/plan/<plan_id>.kml/", methods=['GET'])
def plan_kml(account_id, plan_id):
    dao = PlanDao(content, account_id)
    plan = dao.retrieve(plan_id)
    fin = preprocess(StringIO(plan.cdl))
    analyser = CdlFileAnalyser()
    cdl_file = analyser.analyse(fin)
    kml = cdlfile_to_KML(cdl_file, plan_id)
    return kml, 200, {'Content-Type': 'application/vnd.google-earth.kml+xml; charset=utf-8'}
