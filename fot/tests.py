from django.test import TestCase
from .models import Forecast, Employee


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
