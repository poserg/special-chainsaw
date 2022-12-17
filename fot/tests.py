from django.test import TestCase
from .models import Forecast, Employee, Wage


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
