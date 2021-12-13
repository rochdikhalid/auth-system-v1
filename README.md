# custom-auth-system-v1
During the 30-day coding challenge organized by **DonTheDeveloper**, I could build a custom authentication layer with tests using Django, Django Rest Framework, and PostgreSQL. I didn't use something off the shelf, but I created this layer from scratch to learn the internals of Django's auth system and to clearly understand how authentication works under the hood. 

## Installation Walkthrough

1- Make sure you have the latest version of Python installed (prefered).

2- Clone the repository.<br>
3- Open the repository using the command line by copying its path.


4- Create a virtual environment using the following: <br>

`python3 -m venv <name_of_virtualenv>`

5- Activate the virtual environment by running the following:<br>

`<name_of_virtualenv>\Scripts\activate`

6- Install the dependencies as highlighted below using the requirement.txt file:<br>

`pip install -r requirements.txt`

7- Go to auth directory and migrate the existing database tables:<br>

`python manage.py migrate`

8- Run the Django development server:<br>

`python manage.py runserver`

9- Then, feel free to open up Postman for running and testing the following endpoints:

 * Register endpoint: `http://localhost:8000/api/users/register/`
   
 * Password reset request endpoint: `http://localhost:8000/api/users/password-reset-request/`
   
 * Email confirmation endpoint, the link will be sent to the user's email inbox after registration.
   
 * Password reset endpoint, the link will be sent to the user's email to reset the password.
   
 * Login endpoint: `http://localhost:8000/api/users/login/`
   
 * Logout endpoint: `http://localhost:8000/api/users/logout/`
   



