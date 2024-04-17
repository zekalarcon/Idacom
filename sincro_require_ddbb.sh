#! /bin/bash

source env/bin/activate
python manage.py makemigrations
python manage.py migrate
pip install -r requirements.txt
deactivate