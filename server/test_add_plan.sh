curl -i -H "Content-Type: application/json" -X POST -d \
'{ "account_id": 1, 
"vessel_id": "trilogy",  
"season_id": "ssss", 
"plan_id": "pppp",  
"cdl": "this is the cdl"}' \
http://localhost:5000/1/plan/
