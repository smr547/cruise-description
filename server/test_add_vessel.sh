curl -i -H "Content-Type: application/json" -X POST -d \
'{ "account_id": 1, "identifier": "shed", "name": "The Shed", "flag": "Australian", "rego": "1234456", "speed_kts": 5.0}' \
http://localhost:5000/1/vessel/
