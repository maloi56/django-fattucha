from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import ExpressionWrapper, F, FloatField, Sum

from users.models import User


class Products(models.Model):
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128, null=True, blank=True)
    calories = models.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(0)])
    protein = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    fat = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    carbohydrates = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])

    def __str__(self):
        return f'Продукт - {self.name}, бренд - {self.brand}'


class DailyQuerySet(models.QuerySet):
    def get_week_data(self):
        if not self.exists():
            return {'food': [], 'info': [{'protein': 0, 'fat': 0, 'carbs': 0, 'calories': 0},
                                         {'protein': 0, 'fat': 0, 'carbs': 0, 'calories': 0},
                                         {'protein': 0, 'fat': 0, 'carbs': 0, 'calories': 0},
                                         {'protein': 0, 'fat': 0, 'carbs': 0, 'calories': 0}]}
        else:
            food_object = self.first().get_today()
            return {'food': food_object, 'info': food_object.total_sum()}


class DailyReport(models.Model):
    date = models.DateField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    objects = DailyQuerySet.as_manager()

    class Meta:
        unique_together = ["date", "user"]

    def __str__(self):
        return f'Пользователь - {self.user}, дата - {self.date}'

    def get_today(self):
        return FoodInReport.objects.filter(report=self.pk).select_related('product', 'report')

    @staticmethod
    def get_week_objects(user, year, week):
        if not settings.DEBUG:  # Temporary solution
            cache_key = f'week_objects:{user.pk}:{year}:{week}'
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        first_day_of_week = datetime.strptime(f'{year}-{week}-1', "%Y-%W-%w").date()
        dates = {i: {'date': first_day_of_week + timedelta(days=i),
                     'data': (DailyReport.objects.filter(user=user,
                                                         date=first_day_of_week + timedelta(days=i))).get_week_data()}
                 for i in
                 range(7)}
        total_calories = [dates[i]['data']['info'][0]['calories'] for i in range(7)]
        breakfast_calories = [dates[i]['data']['info'][1]['calories'] for i in range(7)]
        lunch_calories = [dates[i]['data']['info'][2]['calories'] for i in range(7)]
        dinner_calories = [dates[i]['data']['info'][3]['calories'] for i in range(7)]
        total_calories = {'total_calories': sum(total_calories), 'breakfast_calories': sum(breakfast_calories),

                          'lunch_calories': sum(lunch_calories), 'dinner_calories': sum(dinner_calories)}

        if not settings.DEBUG:  # Temporary solution
            cache.set(cache_key, (dates, total_calories), timeout=3600)
        return dates, total_calories

    @staticmethod
    def get_or_none(**kwargs):
        try:
            return DailyReport.objects.get(**kwargs)
        except DailyReport.DoesNotExist:
            return None


class FoodQuerySet(models.QuerySet):
    def sum(self):
        result = self.aggregate(
            # Выражение F достает значение из модели без выгрузки в память Python.
            # ExpresstionWrapper обозначает с каким типом данных необходимо вывести переменную
            protein=Sum(ExpressionWrapper(F('weight') * F('product__protein') / 100,
                                          output_field=FloatField()), default=0),
            fat=Sum(ExpressionWrapper(F('weight') * F('product__fat') / 100,
                                      output_field=FloatField()), default=0),
            carbs=Sum(ExpressionWrapper(F('weight') * F('product__carbohydrates') / 100,
                                        output_field=FloatField()), default=0),
            calories=Sum(ExpressionWrapper(F('weight') * F('product__calories') / 100,
                                           output_field=FloatField()), default=0))
        return result

    def total_sum(self):
        total = self.sum()
        total_list = [total] + [
            self.filter(report_type=i).select_related('product').aggregate(
                protein=Sum(ExpressionWrapper(F('weight') * F('product__protein') / 100,
                                              output_field=FloatField()), default=0),
                fat=Sum(ExpressionWrapper(F('weight') * F('product__fat') / 100,
                                          output_field=FloatField()), default=0),
                carbs=Sum(ExpressionWrapper(F('weight') * F('product__carbohydrates') / 100,
                                            output_field=FloatField()), default=0),
                calories=Sum(ExpressionWrapper(F('weight') * F('product__calories') / 100,
                                               output_field=FloatField()), default=0),
            )
            for i in range(0, 3)
        ]
        return total_list


class FoodInReport(models.Model):
    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2
    REPORT_TYPES = (
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин'),
    )

    product = models.ForeignKey(to=Products, on_delete=models.PROTECT)
    weight = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(9999)])
    report = models.ForeignKey(to=DailyReport, on_delete=models.CASCADE)
    report_type = models.SmallIntegerField(choices=REPORT_TYPES)

    objects = FoodQuerySet.as_manager()

    def __str__(self):
        return f'{self.report}, {self.product}, вес - {self.weight}'
