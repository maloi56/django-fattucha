# Generated by Django 4.2.3 on 2023-08-01 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='parent_id',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('parent_id', 'user')},
        ),
        migrations.RemoveField(
            model_name='likes',
            name='path',
        ),
    ]