# CDL web service

Base URL is https://ws.planacruise.online

| Entity |     URL                       | List |Create|Read|Update|Delete|
|--------|-------------------------------|------|------|----|------|------|
|account | /account/                     | GET  |POST  |  X |   X  |   X  |
|account | /account/[acct_id]/           |   X  |  X   | GET|  PUT |DELETE|
|vessel  | /[acct_id]/vessel/            | GET  |POST  |  X |   X  |   X  |
|vessel  | /[acct_id]/vessel/[vess_id]   |   X  |  X   | GET|  PUT |DELETE|
|person  | /[acct_id]/person/            | GET  |POST  |  X |   X  |   X  |
|person  | /[acct_id]/person/[person_id] |   X  |  X   | GET|  PUT |DELETE|
|season  | /[acct_id]/season/            | GET  |POST  |  X |   X  |   X  |
|season  | /[acct_id]/season/[season_id] |   X  |  X   | GET|  PUT |DELETE|
|region  | /[acct_id]/region/            | GET  |POST  |  X |   X  |   X  |
|region  | /[acct_id]/region/[region_id] |   X  |  X   | GET|  PUT |DELETE|
|location| /[acct_id]/loc/               | GET  |POST  |  X |   X  |   X  |
|location| /[acct_id]/loc/[loc_id]       |   X  |  X   | GET|  PUT |DELETE|
|plan    | /[acct_id]/plan/              | GET  |POST  |  X |   X  |   X  |
|plan    | /[acct_id]/plan/[plan_id]     |   X  |  X   | GET|  PUT |DELETE|
|map     | /[acct_id]/map/[plan_id]      | GET  |  X   |  X |   X  |   X  |
|map     | /[acct_id]/map/[plan_id].[fmt]|   X  |  X   | GET|   X  |   X  |


## Notes

1. [fmt] - map formats available are ``kml``

