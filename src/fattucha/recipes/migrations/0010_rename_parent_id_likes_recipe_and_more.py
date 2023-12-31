# Generated by Django 4.2.3 on 2023-08-01 18:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_alter_likes_parent_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='parent_id',
            new_name='recipe',
        ),
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('recipe', 'user')},
        ),
    ]
