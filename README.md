# paas_manager_flask
Flask implementation of simple platform as a service backend challenge.

This will be entirely CLI-based, and thus will have minimal to no UI
involved.

For purposes of this project, to handle rapid prototyping, the following
will be used:
- Flask
- sqlite (relational Databse)


## Instructions for use:
- Command: `python app.py`


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
