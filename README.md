# My Project README

This is a brief description of my project.

## Set up a virtual environment for python,
- Run `mkdir DjangoTest`                                    # create top directory
- Run `cd DjangoTest`                                       # switch to the top directory
- Run `pip3 install virtualenv`                             # install virtual environment package
- Run `virtualenv -p python3 django_test_venv`

## Then activate the environment via
- Run `source django_test_venv/bin/activate`

## Installation
- Clone the repository.
- Run `pip install -r requirements.txt`.

## Migration
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## Usage
- Run `python manage.py runserver` to start the application.

## To run the test cases
- Run `python manage.py test`

## env file
- Create .env file and configure below keys
- 1.DB_NAME - set database name
- 2.DB_HOST - set hostname
- 3.DB_PASSWORD - set database password
- 4.DB_PORT - set port
- 5.DB_USER - set database user
- 6.EMAIL_HOST - set email provider hostname
- 7.EMAIL_USER - set email id
- 8.EMAIL_PASS - set email password
- 9.CELERY_BROKER_URL - set celery broker url
- 10.EXPIRY_TIME - set expiry time for login otp in minutes
- 11.SECRET_KEY  - set django secret key