# CDL web service

Base URL is https://ws.planacruise.online

| Entity |     URL                         | List |Create|Read|Update|Delete| format |
|--------|---------------------------------|------|------|----|------|------|--------|
|account | /account/                       |   X  |POST  |  X |   X  |   X  |Note 1|
|account | /account/[acct_id]/             |   X  |  X   | GET|  PUT |DELETE|``json`` only|
|vessel  | /[acct_id]/vessel/              | GET  |  X   |  X |   X  |   X  |Note 2|
|vessel  | /[acct_id]/vessel/[vess_id]     |   X  | POST | GET|  PUT |DELETE|``json`` only|
|person  | /[acct_id]/person/              | GET  |  X   |  X |   X  |   X  |Note 2|
|person  | /[acct_id]/person/[person_id]   |   X  | POST | GET|  PUT |DELETE|``json`` only|
|season  | /[acct_id]/season/              | GET  |  X   |  X |   X  |   X  |Note 2|
|season  | /[acct_id]/season/[season_id]   |   X  | POST | GET|  PUT |DELETE|``json`` only|
|region  | /[acct_id]/region/              | GET  |  X   |  X |   X  |   X  |Note 2|
|region  | /[acct_id]/region/[region_id]   |   X  | POST | GET|  PUT |DELETE|``json`` only|
|location| /[acct_id]/loc/                 | GET  |  X   |  X |   X  |   X  |Note 2|
|location| /[acct_id]/loc/[loc_id]         |   X  | POST | GET|  PUT |DELETE|``json`` only|
|plan    | /[acct_id]/plan[.fmt]/          | GET  |  X   |  X |   X  |   X  |``json``, ``html``|
|plan    | /[acct_id]/plan/[plan_id]       |   X  | POST | GET|  PUT |DELETE|Note 2|
|map     | /[acct_id]/map/[plan_id].[fmt]  |   X  |  X   | GET|   X  |   X  | ``kml`` only|
|timeline| /[acct_id]/sched/[plan_id].[fmt]|   X  |  X   | GET|   X  |   X  |``md, json, html, pdf``|


## Notes

1. System will always generate a surrogate ID for the ``account`` entity
2. Listing format will default to ``json``. ``html`` also available

