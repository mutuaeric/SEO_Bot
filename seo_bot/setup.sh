#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Start the Django server
python manage.py runserver
