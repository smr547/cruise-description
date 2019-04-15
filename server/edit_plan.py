#!/usr/bin/env python3

import argparse
import requests
import os



parser = argparse.ArgumentParser(description='Edit a cruise')
parser.add_argument('--account', type=int, default=1)
parser.add_argument('plan_id', help='plan identifier')
args = parser.parse_args()

url = 'http://localhost:5000/{}/plan/{}/'.format(args.account, args.plan_id)
response = requests.get(url)
if response.status_code == 200:
    cdl=response.json()['cdl']
    with open("./tempfile.cdl", 'w') as tempfile:
        tempfile.write(cdl)

    os.system("vi ./tempfile.cdl")
    with open("./tempfile.cdl", 'r') as tempfile:
        cdl = tempfile.read()


    url = 'http://localhost:5000/{}/plan/{}.cdl/'.format(args.account, args.plan_id)
    response = requests.put(url, data=cdl)
    print(response.status_code)
else:
    print("{}: {}".format(response.status_code, response.text))
