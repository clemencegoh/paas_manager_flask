# paas_manager_flask
Flask implementation of simple platform as a service backend challenge

## Requirements:
- User:
    - Need to Authenticate with email address and password
    - Create, List, Delete resources
    - Cannot access others' resources
    - Cannot create new resource if quota exceeded
- Admin:
    - Create, List, Delete Users
    - Create, List, Delete Resources
    - Set Quota for any user

## Resources
- Represented by a string with unique ID

## Admin
- Admin must have all user capabilities

## Quota
- Default quota is infinite (not set)

## Error Responses
- Catch and provide responses for any errors
