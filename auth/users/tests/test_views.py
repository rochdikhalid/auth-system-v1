from django.test import TestCase #, Client 
from django.urls import reverse_lazy
from users.models import CustomUser



# Some test settings
class TestConfig(TestCase):

    @classmethod
    def setUpTestData(cls):

        CustomUser.objects.create_user(
            email = 'randomuser0@gmail.com',
            username = 'randomuser0',
            password = '2HJ1vRV0Z&3iP',
        )

    # Every test function will get a "fresh" version of set up objects 
    def setUp(self):
        self.user_data = {
            'email': 'randomuser1@gmail.com',
            'username': 'randomuser1',
            'password': '2HJ1vRV0Z&3iA',
        }

    """
    def setUp(self):
        self.client = Client()
    """

# To test the register view
class TestRegisterView(TestConfig):

    # To test that the register URL is existed at the desired location
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/users/register/')
        self.assertEqual(response.status_code, 200)

    # To test that the register URL is accessible by its name
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('users:register_user'))
        self.assertEqual(response.status_code, 200)

    # To test that the user cannot register without its credentials
    def test_user_cannot_register_without_data(self):
        response = self.client.post('/api/users/register/')
        self.assertEqual(response.status_code, 400)

    # To test that the user can register successfully with correct credentials
    def test_user_can_register_successfully(self):
        response = self.client.post(
            '/api/users/register/',
            self.user_data,
            format = 'json',
        )
        self.assertEqual(response.status_code, 201)        

    # To test that the user cannot register if the email is already existed
    def test_user_cannot_register_if_email_existed(self):
        self.user_data['email'] = 'randomuser0@gmail.com'
        response = self.client.post(
            '/api/users/register/',
            self.user_data,
            format = 'json',
        )
        self.assertEqual(response.status_code, 400)

    # To test that the user cannot register if the username is already existed
    def test_user_cannot_register_if_username_existed(self):
        self.user_data['username'] = 'randomuser0'
        response = self.client.post(
            '/api/users/register/',
            self.user_data,
            format = 'json',
        )
        self.assertEqual(response.status_code, 400)

# To test the password reset request view
class TestPasswordResetRequestView(TestConfig):

    # To test that the mentionel URL is existed at the desired location
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/users/password-reset-request/')
        self.assertEqual(response.status_code, 200)

    # To test that the mentioned URL is accessible by its name
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('users:password-reset-request'))
        self.assertEqual(response.status_code, 200)

    # To test that the user cannot request for a password reser without its credentials
    def test_user_cannot_request_password_reset_without_data(self):
        response = self.client.post('/api/users/password-reset-request/')
        self.assertEqual(response.status_code, 400)

    # To test that the user cannot request for a password reset in case if email not existed
    def test_user_cannot_request_reset_password(self):
        response = self.client.post(
            '/api/users/password-reset-request/',
            {'email': 'randomuser1@gmail.com'},
            format = 'json',
        )
        self.assertEqual(response.status_code, 400)

    # To test that the user can request for a password reset if email is existed
    def test_user_can_request_reset_password(self):
        response = self.client.post(
            '/api/users/password-reset-request/',
            {'email': 'randomuser0@gmail.com'},
            format = 'json',
        )
        self.assertEqual(response.status_code, 200)

# To test the login view
class TestLoginView(TestConfig):

    # To test that the mentioned URL is existed at the desired location
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/users/login/')
        self.assertEqual(response.status_code, 200)

    # To test that the mentioned URL is accessible by its name
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('users:login'))
        self.assertEqual(response.status_code, 200)

    # To test that the user cannot login without its credentials
    def test_user_cannot_login_without_data(self):
        response = self.client.post('/api/users/login/')
        self.assertEqual(response.status_code, 401)

    # To test that the user can login with confirmed email
    def test_user_can_login_with_confirmed_email(self):
        register_response = self.client.post(
            '/api/users/register/',
            self.user_data,
            format = 'json',
        )
        email = register_response.data['email']
        user = CustomUser.objects.get(email = email)
        user.is_active = True
        user.save()
        login_response = self.client.post(
            '/api/users/login/',
            self.user_data,
            format = 'json',
        )
        self.assertEqual(login_response.status_code, 200)

    # To test that the user cannot login with non verified email
    def test_user_cannot_login_with_uncofirmed_email(self):
        register_response = self.client.post(
            '/api/users/register/',
            self.user_data,
            format = 'json',
        )
        login_response = self.client.post(
            '/api/users/login/',
            self.user_data,
            format = 'json',
        )
        self.assertEqual(login_response.status_code, 401)

# To test the logout view
class TestLogoutView(TestConfig):

    # To test that the mentioned URL is existed at the desired location
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/users/logout/')
        self.assertEqual(response.status_code, 200)

    # To test that the mentioned URL is accessible by its name
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse_lazy('users:logout'))
        self.assertEqual(response.status_code, 200)

    # To test that the user cannot logout without credentials
    def test_user_cannot_logout_without_data(self):
        response = self.client.post('/api/users/logout/')
        self.assertEqual(response.status_code, 204)


    
        


    



