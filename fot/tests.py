from django.test import TestCase
from .models import Forecast, Employee, Wage
# from django.db import connection
# from django.test.utils import CaptureQueriesContext
from datetime import datetime, date
import pytz
from django.conf import settings

today_year = date.today().year


class ForecastTestCase(TestCase):

    def test_create_new_wages_after_forecast_created(self):
        Employee.objects.create(first_name='Bob', last_name='Wilson')
        Employee.objects.create(first_name='Nick', last_name='Pope',
                                is_active=False)
        forecat = Forecast.objects.create(name="test forecast")
        self.assertEqual(forecat.wage_set.count(), 1)

    def test_not_create_new_wages_when_forecast_updated(self):
        Employee.objects.create(first_name='Bob', last_name='Wilson')
        Employee.objects.create(first_name='Nick', last_name='Pope',
                                is_active=False)
        forecat = Forecast.objects.create(name="test forecast")
        self.assertEqual(forecat.wage_set.count(), 1)

        forecat.save()
        self.assertEqual(forecat.wage_set.count(), 1)


class WageTestCase(TestCase):

    # def test_calc_net_salary(self):
    #     employee = Employee.objects.create(
    #         first_name='Bob', last_name='Wilson')
    #     wage = Wage.objects.create(
    #         employee=employee,
    #         salary=100,
    #         monthly_premium=20,
    #         quarterly_premium=45)
    #     self.assertEqual(wage.net_salary(), (100+20+45/3)*0.87)

    def test_growth(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        wage1 = Wage.objects.create(
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)
        wage2 = Wage.objects.create(
            employee=employee,
            salary=120,
            quarterly_premium=60)

        self.assertEqual(wage1.growth(), "0 %")
        self.assertEqual(wage2.growth(), str(
            round((120+60/3)*100/(100+20+45/3)-100, 2)) + " %")

    def test_annual_growth(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        tz = pytz.timezone(settings.TIME_ZONE)
        wage1 = Wage.objects.create(
            aprooved=datetime(2021, 4, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)
        wage2 = Wage.objects.create(
            aprooved=datetime(2022, 10, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=120,
            quarterly_premium=60)

        self.assertEqual(wage1.annual_growth(), '-')
        # with CaptureQueriesContext(connection) as ctx:
        #     # code that runs SQL queries
        #     wage2.annual_growth()
        #     print(ctx.captured_queries)
        self.assertEqual(wage2.annual_growth(), str(
            round((120+60/3)*100/(100+20+45/3)-100, 2)) + " %")

    def test_zero_annual_growth(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        tz = pytz.timezone(settings.TIME_ZONE)
        wage1 = Wage.objects.create(
            aprooved=datetime(2020, 10, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        wage2 = Wage.objects.create(
            aprooved=datetime(2022, 4, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)

        self.assertEqual(wage1.annual_growth(), '-')
        self.assertEqual(wage2.annual_growth(), '-')

    def test_annual_growth_by_employee(self):
        employee1 = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        tz = pytz.timezone(settings.TIME_ZONE)
        wage1 = Wage.objects.create(
            aprooved=datetime(2021, 10, 1, 10, 0, 0, tzinfo=tz),
            employee=employee1,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)

        employee2 = Employee.objects.create(
            first_name='Mark', last_name='Spenser')
        wage2 = Wage.objects.create(
            aprooved=datetime(2022, 4, 1, 10, 0, 0, tzinfo=tz),
            employee=employee2,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)

        self.assertEqual(wage1.annual_growth(), '-')
        self.assertEqual(wage2.annual_growth(), '-')


class EmployeeTestCase(TestCase):
    def test_annual_income_from_december(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        tz = pytz.timezone(settings.TIME_ZONE)
        Wage.objects.create(
            aprooved=datetime(today_year - 2, 12, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        Wage.objects.create(
            aprooved=datetime(today_year, 4, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)

        self.assertEqual(employee.annual_income(), [
                [today_year-2, 100.0],
                [today_year-1, 1200.0],
                [today_year, 1515.0],
                [today_year+1, 1620.0],
                [today_year+2, 1620.0],
            ])

    def test_annual_income(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        tz = pytz.timezone(settings.TIME_ZONE)
        Wage.objects.create(
            aprooved=datetime(today_year-2, 12, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        Wage.objects.create(
            aprooved=datetime(today_year-1, 4, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)
        Wage.objects.create(
            aprooved=datetime(today_year-1, 10, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=40,
            quarterly_premium=45)

        self.assertEqual(employee.annual_income(), [
                [today_year-2, 100.0],
                [today_year-1, 1575.0],
                [today_year, 1860.0],
                [today_year+1, 1860.0],
                [today_year+2, 1860.0],
            ])
