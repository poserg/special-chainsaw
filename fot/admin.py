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
    list_display = (
        "employee",
        "created",
        "modified",
        "forecast",
        "position",
        "show_net_salary",
        "salary",
        "monthly_premium",
        "quarterly_premium",
        "rate",
        "district_coefficient",
    )

    list_filter = (
        "forecast",
        "employee",
    )

    def show_net_salary(self, obj):
        return (obj.salary+obj.monthly_premium+obj.quarterly_premium/3)*0.87

    show_net_salary.short_description = "Net Salary"


@admin.register(MarketWage)
class MarketWageAdmin(admin.ModelAdmin):
    ...
