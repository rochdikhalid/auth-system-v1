from django.test import TestCase
from users.models import CustomUser




# TestCase is going to create a temporary clean database which will be detroyed after the unit test stops
class CustomUserTest(TestCase): 

    # To create a user object that we'll use but not modify in any of the tests
    @classmethod
    def setUpTestData(cls):
        
        CustomUser.objects.create_user(
            email = 'randomuser0@gmail.com',
            username = 'randomuser0'
        )

        CustomUser.objects.create_superuser(
            email = 'randomsuperuser0@gmail.com', 
            username = 'randomsuperuser0'
        )

    # To test the email label
    def test_email_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    # To test that the maximum length of email field equals 255 characters
    def test_email_max_length(self):
        custom_user = CustomUser.objects.get(id = 1)
        max_length = custom_user._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    # To test the username label
    def test_username_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    # To test that the maximum length of username field equals to 150 characters
    def test_username_max_length(self):
        custom_user = CustomUser.objects.get(id = 1)
        max_length = custom_user._meta.get_field('username').max_length
        self.assertEqual(max_length, 150)

    # To test is_active label
    def test_is_active_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'is active')

    # To test that the user state is set to inactive after it's registered
    def test_user_is_inactive(self):
        custom_user = CustomUser.objects.get(id = 1)
        user_status = custom_user.is_active
        self.assertEqual(user_status, False)

    # To test that the superuser state is set to active as default
    def test_superuser_is_active(self):
        custom_user = CustomUser.objects.get(id = 2)
        user_status = custom_user.is_active
        self.assertEqual(user_status, True)

    # To test the is_admin label
    def test_is_admin_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('is_admin').verbose_name
        self.assertEqual(field_label, 'is admin')

    # To test that the user is set as non admin after it's registered
    def test_user_is_not_an_admin(self):
        custom_user = CustomUser.objects.get(id = 1)
        user_status = custom_user.is_admin
        self.assertEqual(user_status, False)

    # To test that the superuser is set as admin as default
    def test_superuser_is_admin(self):
        custom_user = CustomUser.objects.get(id = 2)
        user_status = custom_user.is_admin
        self.assertEqual(user_status, True)

    # To test the times_password_changed_label
    def test_times_password_changed_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('times_password_changed').verbose_name
        self.assertEqual(field_label, 'times password changed')

    # To test the created_at label
    def test_created_at_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    # To test the updated_at label
    def test_updated_at_label(self):
        custom_user = CustomUser.objects.get(id = 1)
        field_label = custom_user._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # To test that the object string representation defined by user's email
    def test_string_representaion(self):
        custom_user = CustomUser.objects.get(id = 1)
        exp_representation = f'{custom_user.email}'
        self.assertEqual(str(custom_user), exp_representation)

    # To test that the plural of the model name is set to "users"
    def test_verbose_name_plural(self):
        object_plural = CustomUser._meta.verbose_name_plural
        self.assertEqual(object_plural, 'users')

    



