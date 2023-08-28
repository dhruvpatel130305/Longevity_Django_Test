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

## Migration
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## Usage
- Run `python manage.py runserver` to start the application.

## To run celery command
- Run `celery -A django_test worker -l info`

## To run the test cases
- Run `python manage.py test`

## Github 
- https://github.com/dhruvpatel130305/Longevity_Django_Test

## API Documentation
- https://docs.google.com/document/d/17_9-G_xo77paKlFi3yFkM_dw8fe1SyC5e5ztO7-hutg/edit

## Postman collection link
- https://documenter.getpostman.com/view/21272355/2s9Y5YTNgn

## swagger link
- http://ec2-54-167-17-31.compute-1.amazonaws.com/swagger/
