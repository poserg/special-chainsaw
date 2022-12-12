from django.db import models
from behaviors.behaviors import Timestamped


class Employee(Timestamped):
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}."
        f'{self.patronymic[0] if self.patronymic else ""}.'
        f" - {self.position}"

    class Meta:
        ordering = ['last_name', 'first_name', 'patronymic']


class Wish(Timestamped):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    minimum = models.FloatField()
    comfort = models.FloatField()

    def __str__(self):
        return f"{self.minimum} - {self.comfort}"

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Wishes'


class Forecast(Timestamped):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created']


POSITION_CHOICES = [
    ('Lead', (
        ('LEAD_DEVELOPER', 'Ведущий разработчик'),
        ('LEAD_1S', 'Ведущий разработчик 1С'),
        ('LEAD_SOFTWARE', 'Ведущий разработчик программного обеспечения'),
    )),
    ('Chief', 'Главный разработчик'),
    ('Junior', (
        ('JUNIOR_PROGRAMMER', 'Младший программист'),
        ('JUNIOR_DEVELOPER', 'Младший разработчик'),
        ('JUNIOR_SOFTWARE_DEVELOPER',
         'Младший разработчик программного обеспечения'),
    )),
    ('Junior specialist', (
        ('JUNIOR_DEV_SPECIALIST', 'Младший специалист по разработке'),
        ('JUNIOR_QA_SPECIALIST',
         'Младший специалист по обеспечению качества'),
    )),
    ('Developer', (
        ('DEVELOPER_COMMON', 'Разработчик'),
        ('SOFTWARE_DEVELOPER', 'Разработчик программного обеспечения'),
        ('QA_SPECIALIST', 'Специалист по обеспечению качества'),
    )),
    ('Team Leader', (
        ('DEVELOPMENT_TEAM_LEADER', 'Руководитель группы разработки'),
        ('SOFTWARE_DEVELOPMENT_TEAM_LEADER',
         'Руководитель группы разработки ПО'),
    )),
    ('DEPARTMENT_HEAD', 'Руководитель отдела'),
    ('Senior', (
        ('SENIOR_DEVELOPER', 'Старший разработчик'),
        ('SENIOR_SOFTWARE_DEVELOPER', 'Старший разработчик ПО'),
        ('SENIOR_SOFTWARE_DEVELOPER_FULL',
         'Старший разработчик программного обеспечения'),
    )),
    ('EXPERT', 'Эксперт разработчик'),
]


class Wage(Timestamped):
    forecast = models.ForeignKey(Forecast, on_delete=models.PROTECT,
                                 blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)
    salary = models.FloatField()
    monthly_premium = models.FloatField(blank=True, null=True)
    quarterly_premium = models.FloatField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    rate = models.FloatField(default=1)
    district_coefficient = models.FloatField(default=1)

    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
    )

    def __str__(self):
        return ', '.join((map(str, (self.salary,
                          self.monthly_premium, self.quarterly_premium))))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['forecast', 'employee'],
                name='unique_forecast_employee_combination',
            )
        ]


class MarketWage(Timestamped):
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
    )
    wage = models.FloatField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.position} - {self.wage}'
