# Generated by Django 3.2.5 on 2021-08-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.TextField(max_length=60, unique=True),
        ),
    ]