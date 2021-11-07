# AgileEngine_Bootcamp

# Virtual wallet API

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)


## General Info
The application is based on Django Rest Framework(DRF) and contains 
implemented virtual wallet logic.

## Technologies
1. Django
2. Django REST Framework (DRF)
3. Simple JWT

## Installation
### Before running project
- create local env file
- build containers: `make compose_build`
- run project: `make compose_up`

### When project is running
- Apply db migrations `make migrations`, then `make migrate`
- Create superuser `make superuser`. After all you will be able to login into admin panel
- Be happy :)

#### Create new app
`make app name=<app_name>`

### All commands you can find in `Makefile`
