from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from employee.models import User
from .models import Table, Reservation
from datetime import datetime


# Test list tables
class TestListTables(TestCase):
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

        # create tables
        Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=12)
        Table.objects.create(created_by=admin_user, table_number=2, number_of_seats=12)
        Table.objects.create(created_by=admin_user, table_number=3, number_of_seats=12)
        Table.objects.create(created_by=admin_user, table_number=4, number_of_seats=12)
        Table.objects.create(created_by=admin_user, table_number=5, number_of_seats=12)

    def test_list_tables_with_valid_data_and_admin_user_200_ok(self):
        list_tables = self.admin_client.get(
            reverse('list-tables'),
            data={},
        )
        self.assertEqual(list_tables.status_code, 200)
        self.assertEqual(list_tables.data['count'], 5)

    def test_list_tables_with_valid_data_and_unauthorized_user_401(self):
        list_tables = self.unauthorized_client.get(
            reverse('list-tables'),
            data={},
        )
        self.assertEqual(list_tables.status_code, 401)

    def test_list_tables_with_valid_data_and_employee_user_403(self):
        list_tables = self.employee_client.get(
            reverse('list-tables'),
            data={},
        )
        self.assertEqual(list_tables.status_code, 403)


# Test create table
class TestCreateTable(TestCase):
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

        # create table
        Table.objects.create(created_by=admin_user, table_number=10, number_of_seats=12)

    def test_create_table_with_valid_data_and_admin_user_201_created(self):
        create_table = self.admin_client.post(
            reverse('create-table'),
            data={'table_number': 1, 'number_of_seats': 12},
        )
        self.assertEqual(create_table.status_code, 201)

    def test_create_table_with_exist_table_number_and_admin_user_400_bad_request(self):
        create_table = self.admin_client.post(
            reverse('create-table'),
            data={'table_number': 10, 'number_of_seats': 12},
        )
        self.assertEqual(create_table.status_code, 400)

    def test_create_table_with_number_of_seats_more_than_12_and_admin_user_400_bad_request(self):
        create_table = self.admin_client.post(
            reverse('create-table'),
            data={'table_number': 1, 'number_of_seats': 13},
        )
        self.assertEqual(create_table.status_code, 400)

    def test_create_table_with_number_of_seats_less_than_1_and_admin_user_400_bad_request(self):
        create_table = self.admin_client.post(
            reverse('create-table'),
            data={'table_number': 1, 'number_of_seats': 0},
        )
        self.assertEqual(create_table.status_code, 400)

    def test_create_table_without_data_and_admin_user_400_bad_request(self):
        create_table = self.admin_client.post(
            reverse('create-table'),
            data={},
        )
        self.assertEqual(create_table.status_code, 400)

    def test_create_table_with_valid_data_and_unauthorized_user_401(self):
        create_table = self.unauthorized_client.post(
            reverse('create-table'),
            data={'table_number': 1, 'number_of_seats': 12},
        )
        self.assertEqual(create_table.status_code, 401)

    def test_create_table_with_valid_data_and_employee_user_403(self):
        create_table = self.employee_client.post(
            reverse('create-table'),
            data={'table_number': 1, 'number_of_seats': 12},
        )
        self.assertEqual(create_table.status_code, 403)


# Test delete table
class TestDeleteTable(TestCase):
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

        # create table
        self.table_without_reservation = Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=12)
        self.table_with_reservation = Table.objects.create(created_by=admin_user, table_number=2, number_of_seats=12)
        Reservation.objects.create(table=self.table_with_reservation, start_time='12:00', end_time='13:00',
                                   date='2200-01-01', )

    def test_delete_table_without_reservation_and_admin_user_204(self):
        delete_table = self.admin_client.delete(
            reverse('delete-table', kwargs={'pk': self.table_without_reservation.table_number}),
            data={},
        )
        self.assertEqual(delete_table.status_code, 204)

    # def test_delete_table_with_reservation_and_admin_user_400_bad_request(self):
    #     delete_table = self.admin_client.delete(
    #         reverse('delete-table', kwargs={'pk': self.table_with_reservation.table_number}),
    #         data={},
    #     )
    #     self.assertEqual(delete_table.status_code, 400)

    def test_delete_table_with_invalid_table_number_and_admin_user_404(self):
        delete_table = self.admin_client.delete(
            reverse('delete-table', kwargs={'pk': 0}),
            data={},
        )
        self.assertEqual(delete_table.status_code, 404)

    def test_delete_table_without_reservation_and_unauthorized_user_401(self):
        delete_table = self.unauthorized_client.delete(
            reverse('delete-table', kwargs={'pk': self.table_without_reservation.table_number}),
            data={},
        )
        self.assertEqual(delete_table.status_code, 401)

    def test_delete_table_with_valid_data_and_employee_user_403(self):
        delete_table = self.employee_client.delete(
            reverse('delete-table', kwargs={'pk': self.table_without_reservation.table_number}),
            data={},
        )
        self.assertEqual(delete_table.status_code, 403)


# Test reserve table
class TestReserveTable(TestCase):
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

        # create table
        self.table1 = Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=2)
        self.table2 = Table.objects.create(created_by=admin_user, table_number=2, number_of_seats=12)
        # reserve table
        Reservation.objects.create(table=self.table1, start_time='12:00', end_time='13:00',
                                   date='2200-01-01', )

    def test_reserve_table_with_valid_data_and_admin_user_201_created(self):
        reserve_table = self.admin_client.post(
            reverse('reserve-table'),
            data={
                'start_time': '14:00',
                'end_time': '15:00',
                'date': '2030-02-02',
                'table': self.table1.table_number
            },
        )
        self.assertEqual(reserve_table.status_code, 201)

    def test_reserve_table_in_slot_time_with_another_reservation_and_admin_user_400_bad_request(self):
        reserve_table = self.admin_client.post(
            reverse('reserve-table'),
            data={
                'start_time': '12:30',
                'end_time': '12:45',
                'date': '2200-01-01',
                'table': self.table1.table_number
            },
        )
        self.assertEqual(reserve_table.status_code, 400)

    def test_reserve_table_in_past_and_admin_user_400_bad_request(self):
        reserve_table = self.admin_client.post(
            reverse('reserve-table'),
            data={
                'start_time': '12:30',
                'end_time': '12:45',
                'date': '2000-01-01',
                'table': self.table1.table_number
            },
        )
        self.assertEqual(reserve_table.status_code, 400)

    def test_reserve_table_with_valid_data_and_unauthorized_user_401(self):
        reserve_table = self.unauthorized_client.post(
            reverse('reserve-table'),
            data={
                'start_time': '14:00',
                'end_time': '15:00',
                'date': '2030-02-02',
                'table': self.table1.table_number
            },
        )
        self.assertEqual(reserve_table.status_code, 401)

    def test_reserve_table_with_valid_data_and_employee_user_201(self):
        reserve_table = self.employee_client.post(
            reverse('reserve-table'),
            data={
                'start_time': '14:00',
                'end_time': '15:00',
                'date': '2030-02-02',
                'table': self.table1.table_number
            },
        )
        self.assertEqual(reserve_table.status_code, 201)


# Test list all reservation
class TestListAllReservation(TestCase):
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

        # create tables
        self.table1 = Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=12)
        # create reservations
        Reservation.objects.create(table=self.table1, start_time='12:00', end_time='12:30',
                                   date='2200-01-01', )
        Reservation.objects.create(table=self.table1, start_time='12:31', end_time='13:00',
                                   date='2200-01-01', )
        Reservation.objects.create(table=self.table1, start_time='13:05', end_time='13:15',
                                   date='2200-01-01', )
        Reservation.objects.create(table=self.table1, start_time='13:25', end_time='13:35',
                                   date='2200-01-01', )
        Reservation.objects.create(table=self.table1, start_time='14:40', end_time='14:50',
                                   date='2200-01-01', )

    def test_list_all_reservations_with_valid_data_and_admin_user_200_ok(self):
        list_all_reservations = self.admin_client.get(
            reverse('list-all-reservations'),
            data={},
        )
        self.assertEqual(list_all_reservations.status_code, 200)
        self.assertEqual(list_all_reservations.data['count'], 5)

    def test_list_all_reservations_with_valid_data_and_unauthorized_user_401(self):
        list_all_reservations = self.unauthorized_client.get(
            reverse('list-all-reservations'),
            data={},
        )
        self.assertEqual(list_all_reservations.status_code, 401)

    def test_list_all_reservations_with_valid_data_and_employee_user_403(self):
        list_all_reservations = self.employee_client.get(
            reverse('list-all-reservations'),
            data={},
        )
        self.assertEqual(list_all_reservations.status_code, 403)


# Test list today reservation
class TestListTodayReservation(TestCase):
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

        # create tables
        self.table1 = Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=12)
        # create reservations
        Reservation.objects.create(table=self.table1, start_time='12:00', end_time='12:30',
                                   date=datetime.now().date(), )
        Reservation.objects.create(table=self.table1, start_time='12:31', end_time='13:00',
                                   date=datetime.now().date(), )
        Reservation.objects.create(table=self.table1, start_time='13:05', end_time='13:15',
                                   date=datetime.now().date(), )
        Reservation.objects.create(table=self.table1, start_time='13:25', end_time='13:35',
                                   date=datetime.now().date(), )
        Reservation.objects.create(table=self.table1, start_time='14:40', end_time='14:50',
                                   date=datetime.now().date(), )

    def test_list_today_reservations_with_valid_data_and_admin_user_200_ok(self):
        list_today_reservations = self.admin_client.get(
            reverse('list-today-reservations'),
            data={},
        )
        self.assertEqual(list_today_reservations.status_code, 200)
        self.assertEqual(list_today_reservations.data['count'], 5)

    def test_list_today_reservations_with_valid_data_and_unauthorized_user_401(self):
        list_today_reservations = self.unauthorized_client.get(
            reverse('list-today-reservations'),
            data={},
        )
        self.assertEqual(list_today_reservations.status_code, 401)

    def test_list_today_reservations_with_valid_data_and_employee_user_200(self):
        list_today_reservations = self.employee_client.get(
            reverse('list-today-reservations'),
            data={},
        )
        self.assertEqual(list_today_reservations.status_code, 200)


# Test delete reservation for current working day
class TestDeleteReservation(TestCase):
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

        # create tables
        self.table1 = Table.objects.create(created_by=admin_user, table_number=1, number_of_seats=12)
        # create reservations
        self.reservation_for_current_working_day = Reservation.objects.create(table=self.table1, start_time='12:00',
                                                                              end_time='12:30',
                                                                              date=datetime.now().date(), )
        self.reservation_for_future = Reservation.objects.create(table=self.table1, start_time='12:31',
                                                                 end_time='13:00',
                                                                 date='2200-01-01', )
        self.reservation_in_past = Reservation.objects.create(table=self.table1, start_time='12:31',
                                                              end_time='13:00',
                                                              date='2000-01-01', )

    def test_delete_reservation_for_current_working_day_with_admin_user_204(self):
        delete_reservation = self.admin_client.delete(
            reverse('delete-reservation', kwargs={'pk': self.reservation_for_current_working_day.pk}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 204)

    def test_delete_reservation_for_future_day_with_admin_user_404(self):
        delete_reservation = self.admin_client.delete(
            reverse('delete-reservation', kwargs={'pk': self.reservation_for_future.pk}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 404)

    def test_delete_reservation_in_past_day_with_admin_user_404(self):
        delete_reservation = self.admin_client.delete(
            reverse('delete-reservation', kwargs={'pk': self.reservation_in_past.pk}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 404)

    def test_delete_reservation_with_invalid_reservation_number_and_admin_user_404(self):
        delete_reservation = self.admin_client.delete(
            reverse('delete-reservation', kwargs={'pk': 0}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 404)

    def test_delete_reservation_without_reservation_and_unauthorized_user_401(self):
        delete_reservation = self.unauthorized_client.delete(
            reverse('delete-reservation', kwargs={'pk': self.reservation_for_current_working_day.pk}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 401)

    def test_delete_reservation_with_valid_data_and_employee_user_204(self):
        delete_reservation = self.employee_client.delete(
            reverse('delete-reservation', kwargs={'pk': self.reservation_for_current_working_day.pk}),
            data={},
        )
        self.assertEqual(delete_reservation.status_code, 204)

# Test check available time slots
