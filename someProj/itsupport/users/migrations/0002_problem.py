# Generated by Django 4.1.7 on 2023-03-27 14:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_description', models.CharField(max_length=255)),
                ('problem_type', models.CharField(choices=[('printer', 'Printer'), ('internet', 'Internet'), ('pc', 'PC'), ('other', 'Other')], max_length=20)),
                ('floor', models.PositiveSmallIntegerField(choices=[(1, 'First floor'), (2, 'Second floor')])),
                ('room_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
