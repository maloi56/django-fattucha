# Generated by Django 4.2.3 on 2023-08-01 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_likes_parent_id_alter_likes_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likes',
        ),
    ]