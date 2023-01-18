from django import forms
from django.contrib import admin
from .models import Employee, Wish, Forecast, Wage, \
    MarketWage
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )

    fields = [
        ('first_name', 'last_name'),
        'email',
        'income_growth',
    ]

    def income_growth(self, instance):
        return format_html_join(
            mark_safe('<br>'),
            '{}',
             ((income,) for income in instance.annual_income()),
        )
    income_growth.allow_tags = True

    readonly_fields = ('income_growth', )


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
        "annual_growth",
        "aprooved",
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
