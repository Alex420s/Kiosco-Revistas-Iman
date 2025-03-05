#!/bin/sh

# Crear superusuario con los parámetros especificados en el contenedor.
# python code/manage.py createsuperuser --username=Alex12  --phone_number=556201773433
# Realizar migraciones
python code/manage.py makemigrations 
python code/manage.py migrate
python code/manage.py runserver 0.0.0.0:8000

