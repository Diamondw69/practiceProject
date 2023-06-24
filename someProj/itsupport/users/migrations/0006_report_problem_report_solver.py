# Generated by Django 4.1.7 on 2023-04-01 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='problem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.problem'),
        ),
        migrations.AddField(
            model_name='report',
            name='solver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]