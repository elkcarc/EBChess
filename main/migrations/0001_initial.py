# Generated by Django 2.1.15 on 2020-04-07 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_event', models.CharField(default='No Event', max_length=200)),
                ('game_site', models.CharField(default='On-line', max_length=200)),
                ('game_published', models.DateTimeField(default=datetime.datetime(2020, 4, 7, 3, 2, 27, 196822), verbose_name='date played')),
                ('game_round', models.CharField(default=1, max_length=20)),
                ('game_white', models.CharField(max_length=200)),
                ('game_black', models.CharField(max_length=200)),
                ('game_result', models.CharField(max_length=20)),
                ('game_content', models.TextField()),
            ],
        ),
    ]
