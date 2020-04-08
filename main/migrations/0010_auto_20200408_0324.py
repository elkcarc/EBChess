# Generated by Django 3.0.5 on 2020-04-08 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200408_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='active',
            name='last_move',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 3, 24, 6, 453571), verbose_name='last move'),
        ),
        migrations.AlterField(
            model_name='ai',
            name='last_move',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 3, 24, 6, 453571), verbose_name='last move'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='challenge_issued',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 3, 24, 6, 453571), verbose_name='date issued'),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 8, 3, 24, 6, 452574), verbose_name='date played'),
        ),
    ]
