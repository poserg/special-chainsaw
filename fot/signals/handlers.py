from django.db.models.signals import post_save
from django.dispatch import receiver
from fot.models import Forecast, Employee, Wage


@receiver(post_save, sender=Forecast, dispatch_uid="create_forecasts_wages")
def create_forecasts_wages(sender, instance, **kwargs):
    if instance.wage_set.count() > 0:
        return
    employes = Employee.objects.filter(is_active=True)
    for employee in employes:
        Wage.objects.create(forecast=instance, employee=employee, salary=0)
