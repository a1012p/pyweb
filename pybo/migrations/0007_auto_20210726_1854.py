# Generated by Django 3.2.5 on 2021-07-26 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pybo', '0006_auto_20210725_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_answer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pybo.question'),
        ),
    ]