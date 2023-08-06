# Generated by Django 4.2.3 on 2023-07-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_sex_alter_user_activity_delete_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activity',
            field=models.FloatField(blank=True, choices=[(None, 'Выберите значение вашей активности'), (1.2, 'Минимальный (сидячий образ жизни)'), (1.375, 'Низкий (редко занимаетесь спортом)'), (1.55, 'Средний (занимаетесь спортом 3-5 раз в неделю)'), (1.725, 'Высокий (интенсивные тренировки 6-7 раз в неделю)'), (1.9, 'Очень высокий (физическая работа и активность)')], null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.SmallIntegerField(blank=True, choices=[(None, 'Выберите пол'), (0, 'Мужской'), (1, 'Женский')], null=True),
        ),
    ]