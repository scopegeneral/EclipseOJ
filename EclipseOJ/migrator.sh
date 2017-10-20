#!/bin/bash

python3 manage.py makemigrations accounts
python3 manage.py makemigrations contests
python3 manage.py makemigrations homepage
python3 manage.py makemigrations judge
python3 manage.py makemigrations problems
python3 manage.py makemigrations profiles
python3 manage.py makemigrations discuss
python3 manage.py makemigrations
python3 manage.py migrate
