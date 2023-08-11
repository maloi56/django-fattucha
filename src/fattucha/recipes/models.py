from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from diary.models import Products
from users.models import User


class RecipeCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    CONSIDERATION = 0
    APPROVED = 1

    RECIPE_STATUS_CHOICES = (
        (CONSIDERATION, 'На рассмотрении'),
        (APPROVED, 'Одобрено'),
    )

    name = models.CharField(max_length=48)
    description = models.TextField(max_length=1024)
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT)
    portion = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    time_to_cook = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
    category = models.ForeignKey(to=RecipeCategory, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='recipes_images')
    status = models.IntegerField(choices=RECIPE_STATUS_CHOICES, default=CONSIDERATION)

    def __str__(self):
        return f'{self.name} от {self.creator.username}'

    def get_ingredients(self):
        return self.ingredients.all().select_related('product')

    def get_portion_info(self):
        ingredients = self.get_ingredients()
        result = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
        for ingregient in ingredients:
            result['calories'] += ingregient.product.calories / 100 * ingregient.weight
            result['protein'] += ingregient.product.protein / 100 * ingregient.weight
            result['fat'] += ingregient.product.fat / 100 * ingregient.weight
            result['carbs'] += ingregient.product.carbohydrates / 100 * ingregient.weight
        return result


class Ingredient(models.Model):
    product = models.ForeignKey(to=Products, on_delete=models.PROTECT)
    weight = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(9999)])
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return f'{self.product} в {self.recipe}'


class CookingSteps(models.Model):
    step = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    how_to_cook = models.TextField()
    image = models.ImageField(upload_to='recipes_steps', null=True, blank=True)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='steps')


class LikesQuerySet(models.QuerySet):
    def get_sum_likes(self):
        return self.count()


class Likes(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='likes')

    objects = LikesQuerySet.as_manager()

    class Meta:
        unique_together = ('recipe', 'user')
