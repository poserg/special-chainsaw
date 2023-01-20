from django.test import TestCase
from .models import Forecast, Employee, Wage
# from django.db import connection
# from django.test.utils import CaptureQueriesContext
from datetime import datetime, date
import pytz
from django.conf import settings

today_year = date.today().year
tz = pytz.timezone(settings.TIME_ZONE)


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


def get_datetime(year, month):
    return datetime(year, month, 1, 10, 0, 0, tzinfo=tz)


class WageTestCase(TestCase):

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
        wage1 = Wage.objects.create(
            aprooved=get_datetime(2021, 4),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)
        wage2 = Wage.objects.create(
            aprooved=get_datetime(2022, 10),
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
        wage1 = Wage.objects.create(
            aprooved=get_datetime(2020, 10),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        wage2 = Wage.objects.create(
            aprooved=get_datetime(2022, 4),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)

        self.assertEqual(wage1.annual_growth(), '-')
        self.assertEqual(wage2.annual_growth(), '-')

    def test_annual_growth_by_employee(self):
        employee1 = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        wage1 = Wage.objects.create(
            aprooved=get_datetime(2021, 10),
            employee=employee1,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)

        employee2 = Employee.objects.create(
            first_name='Mark', last_name='Spenser')
        wage2 = Wage.objects.create(
            aprooved=get_datetime(2022, 4),
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
        Wage.objects.create(
            aprooved=get_datetime(today_year-2, 12),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        Wage.objects.create(
            aprooved=get_datetime(today_year, 4),
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
        Wage.objects.create(
            aprooved=get_datetime(today_year-2, 12),
            employee=employee,
            salary=100,
            monthly_premium=0,
            quarterly_premium=0)
        Wage.objects.create(
            aprooved=get_datetime(today_year-1, 4),
            employee=employee,
            salary=100,
            monthly_premium=20,
            quarterly_premium=45)
        Wage.objects.create(
            aprooved=get_datetime(today_year-1, 10),
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

    def test_two_income_at_month(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        Wage.objects.create(
            aprooved=get_datetime(2020, 1),
            employee=employee,
            salary=1,
            monthly_premium=0)
        Wage.objects.create(
            aprooved=datetime(2020, 5, 1, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=10,
            monthly_premium=0)
        Wage.objects.create(
            aprooved=datetime(2020, 5, 2, 10, 0, 0, tzinfo=tz),
            employee=employee,
            salary=100,
            monthly_premium=0)
        Wage.objects.create(
            aprooved=get_datetime(2020, 10),
            employee=employee,
            salary=1000,
            monthly_premium=0)

        self.assertEqual(employee.annual_income()[0], [2020, 3504.0])
        self.assertEqual(employee.annual_income()[3], [2023, 12000.0])

    def test_annual_income_with_percent(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        Wage.objects.create(
            aprooved=get_datetime(2020, 1),
            employee=employee,
            salary=10,
            monthly_premium=0)
        Wage.objects.create(
            aprooved=get_datetime(2021, 1),
            employee=employee,
            salary=12,
            monthly_premium=0)
        Wage.objects.create(
            aprooved=get_datetime(2022, 5),
            employee=employee,
            salary=15,
            monthly_premium=0)
        self.assertEqual(
            employee.annual_income_with_percent()[0],
            [2020, 120.0, 100]
        )
        self.assertEqual(
            employee.annual_income_with_percent()[1], 
            [2021, 144.0, 20]
        )
        self.assertEqual(
            employee.annual_income_with_percent()[2],
            [2022, 168.0, 17]
        )
        self.assertEqual(
            employee.annual_income_with_percent()[3],
            [2023, 180.0, 7]
        )
        self.assertEqual(
            employee.annual_income_with_percent()[4],
            [2024, 180.0, 0]
        )

    def test_annual_income_field(self):
        employee = Employee.objects.create(
            first_name='Bob', last_name='Wilson')
        Wage.objects.create(
            aprooved=get_datetime(2020, 1),
            employee=employee,
            salary=10,
            monthly_premium=0)
        result = employee.annual_income_field()
        self.assertEqual(result[0], [2020, "100%"])
        self.assertEqual(result[1], [2021, "0%"])
