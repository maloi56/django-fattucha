# Generated by Django 4.2.3 on 2023-07-31 14:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredient_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookingSteps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('how_to_cook', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes_steps')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='how_to_cook',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='weight',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='portion',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_to_cook',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
        ),
    ]
