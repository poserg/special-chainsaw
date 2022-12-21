from django import forms
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


class YourModelForm(forms.ModelForm):

    extra_field = forms.CharField(required=False)

    # def save(self, commit=True):
    #     extra_field = self.cleaned_data.get('extra_field', None)
    #     # ...do something with extra_field here...
    #     return super(YourModelForm, self).save(commit=commit)

    class Meta:
        model = Wage
        # fields = [
        #     'employee',
        #     'forecast',
        # ]
        fields = '__all__'


@admin.register(Wage)
class WageAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        # "forecast",
        "position",
        "show_net_salary",
        "growth",
        "salary",
        "monthly_premium",
        "quarterly_premium",
        "rate",
        "district_coefficient",
        "created",
        "modified",
    )

    list_filter = (
        "forecast",
        "employee",
    )

    def show_net_salary(self, obj):
        return (obj.salary+obj.monthly_premium+obj.quarterly_premium/3)*0.87

    show_net_salary.short_description = "Net Salary"

    readonly_fields = (
        # 'extra_field',
    )

    form = YourModelForm

    # fieldsets = (
    #     (None, {
    #         'fields': ('employee', 'salary', 'extra_field',),
    #     }),
    # )
    list_editable = (
        'position',
        'salary',
        "monthly_premium",
        "quarterly_premium",
    )


@admin.register(MarketWage)
class MarketWageAdmin(admin.ModelAdmin):
    ...
