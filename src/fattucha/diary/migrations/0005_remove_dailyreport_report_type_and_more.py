# Generated by Django 4.2.3 on 2023-07-10 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_dailyreport_report_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyreport',
            name='report_type',
        ),
        migrations.AddField(
            model_name='foodinreport',
            name='report_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='diary.reporttype'),
            preserve_default=False,
        ),
    ]
