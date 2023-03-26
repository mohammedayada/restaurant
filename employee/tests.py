from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


# Test employee login
class TestEmployeeLogin(TestCase):
    def setUp(self):
        # create employee user
        self.client = APIClient()
        employee_user = User.objects.create_user(user_number=9090, password='adminadmin', role='Employee')

    def test_employee_register_with_valid_data_200_ok(self):
        user_login = self.client.post(
            reverse('token_obtain_pair'),
            data={'user_number': 9090, 'password': 'adminadmin'},
        )
        self.assertEqual(user_login.status_code, 200)

    def test_employee_register_with_invalid_user_number_401_unauthorized(self):
        user_login = self.client.post(
            reverse('token_obtain_pair'),
            data={'user_number': 900, 'password': 'adminadmin'},
        )
        self.assertEqual(user_login.status_code, 401)

    def test_employee_register_with_invalid_password_401_unauthorized(self):
        user_login = self.client.post(
            reverse('token_obtain_pair'),
            data={'user_number': 9090, 'password': 'admin'},
        )
        self.assertEqual(user_login.status_code, 401)

    def test_employee_register_without_data_400_bad_request(self):
        user_login = self.client.post(
            reverse('token_obtain_pair'),
            data={},
        )
        self.assertEqual(user_login.status_code, 400)


# Test employee register
class TestEmployeeRegister(TestCase):
    def setUp(self):
        # create Admin user
        self.admin_client = APIClient()
        admin_user = User.objects.create_superuser(user_number=9999, password='admin', role='Admin')
        # login with admin_user
        self.admin_client.login(user_number=9999, password='admin')
        refresh = RefreshToken.for_user(admin_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # create employee user
        self.employee_client = APIClient()
        employee_user = User.objects.create_user(user_number=9090, password='admin', role='Employee')
        # login with admin_user
        self.employee_client.login(user_number=9090, password='admin')
        refresh = RefreshToken.for_user(employee_user)
        self.employee_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # create unauthorized client
        self.unauthorized_client = APIClient()

    def test_employee_register_with_valid_data_and_admin_user_201_created(self):
        register_employee = self.admin_client.post(
            reverse('employee-register'),
            data={'user_number': 1000, 'password': 'employee', 'password2': 'employee', 'role': 'Employee'},
        )
        self.assertEqual(register_employee.status_code, 201)

    def test_employee_register_with_invalid_data_and_admin_user_400_bad_request(self):
        register_employee = self.admin_client.post(
            reverse('employee-register'),
            data={'user_number': 100, 'password': 'empl', 'password2': 'empl', 'role': 'Employee'},
        )
        self.assertEqual(register_employee.status_code, 400)

    def test_employee_register_with_user_number_exists_and_admin_user_400_bad_request(self):
        register_employee = self.admin_client.post(
            reverse('employee-register'),
            data={'user_number': 9999, 'password': 'employee', 'password2': 'employee', 'role': 'Employee'},
        )
        self.assertEqual(register_employee.status_code, 400)

    def test_employee_register_with_valid_data_and_unauthorized_user_401(self):
        register_employee = self.unauthorized_client.post(
            reverse('employee-register'),
            data={'user_number': 1000, 'password': 'employee', 'password2': 'employee', 'role': 'Employee'},
        )
        self.assertEqual(register_employee.status_code, 401)

    def test_employee_register_with_valid_data_and_employee_user_403(self):
        register_employee = self.employee_client.post(
            reverse('employee-register'),
            data={'user_number': 1000, 'password': 'employee', 'password2': 'employee', 'role': 'Employee'},
        )
        self.assertEqual(register_employee.status_code, 403)
