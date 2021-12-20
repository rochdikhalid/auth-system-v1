# custom-auth-system-v1
During the 30-day coding challenge organized by **DonTheDeveloper**, I could build a custom authentication layer with tests using **Django**, **Django Rest Framework**, and **PostgreSQL**. I didn't use something off the shelf, but I created this layer from scratch to learn the internals of **Django**'s auth system and to clearly understand how authentication works under the hood. 

## Installation Walkthrough

1- The project backend was generated with [Django](https://github.com/django/django) version 3.2.9, make sure you have the latest version of **Python** installed (prefered).

2- Create a virtual environment using the following: 

    python3 -m venv <name_of_virtualenv>

3- Activate the virtual environment by running the following:

    <name_of_virtualenv>\Scripts\activate

4- Install the dependencies as highlighted below using the **requirement.txt** file:

    pip install -r requirements.txt

5- Go to **auth** directory and migrate the existing database tables:

    python manage.py migrate

6- Run the **Django** development server:

    python manage.py runserver

7- Then, feel free to open up Postman for running and testing the following endpoints:

 * **Register** endpoint: **http://localhost:8000/api/users/register/**
   
 * **Password** reset request endpoint: **http://localhost:8000/api/users/password-reset-request/**
   
 * **Email confirmation** endpoint, the link will be sent to the user's email inbox after registration.
   
 * **Password reset** endpoint, the link will be sent to the user's email to reset the password.
   
 * **Login** endpoint: **http://localhost:8000/api/users/login/**
   
 * **Logout** endpoint: **http://localhost:8000/api/users/logout/**
   



