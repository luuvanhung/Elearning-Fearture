#!/bin/bash

echo 'reset DB...'

python manage.py migrate api_seat_map zero
python manage.py migrate api_session zero
python manage.py migrate api_office zero
python manage.py migrate api_skill zero
python manage.py migrate api_oauth2 zero
python manage.py migrate oauth2_provider zero
python manage.py migrate api_event zero
python manage.py migrate api_user_lunch zero
python manage.py migrate api_lunch zero
python manage.py migrate api_providers zero
python manage.py migrate api_workday zero
python manage.py migrate api_team zero
python manage.py migrate api_user zero
python manage.py migrate auth zero
python manage.py migrate contenttypes zero
python manage.py migrate sessions zero
python manage.py migrate binary_database_files zero

echo 'successfully'
