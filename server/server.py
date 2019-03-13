#!/usr/bin/env python3

import os
from flask import Flask, request
app = Flask(__name__)

content = "/home/smring/planacruise/content"

@app.route("/hello", methods=['POST', 'GET'])
def hello():
    print(request)
    for h in request.headers:
        print(h)
    print(request.get_data())
    return  "Hello World"

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
