curl -i -H "Content-Type: application/json" -X POST -d \
'{ "account_id":1, 
            "identifier":"fas", 
            "surname":"Smith", 
            "first_names":"Frederick Alexander",
            "address":"17 Constitution Ave, Canberra, ACT 2612",
            "email": "fred.smith@gmail.com",
            "phone": "+61234567273",
            "gender": "MALE",
            "passport_no": "P1234543212",
            "passport_country": "Australia",
            "passport_issued": "2012-10-25",
            "passport_expiry": "2022-10-25",
            "skills": "",
            "blood_group": "O+ve",
            "allergies": "",
            "medication": "",
            "quals": "Yachtmaster, senior first aid" }' \
http://localhost:5000/1/person/
