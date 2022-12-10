from django.contrib import admin
from .models import Employee, Wish, Forecast, Wage, \
    MarketWage


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    ...


@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    ...


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    ...


@admin.register(Wage)
class WageAdmin(admin.ModelAdmin):
    ...


@admin.register(MarketWage)
class MarketWageAdmin(admin.ModelAdmin):
    ...
