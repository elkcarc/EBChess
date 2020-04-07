# Generated by Django 2.1.15 on 2020-04-07 09:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200407_0322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('challenge_id', models.AutoField(primary_key=True, serialize=False)),
                ('challenge_user1', models.CharField(default='Not Set', max_length=200)),
                ('challenge_user2', models.CharField(default='Not Set', max_length=200)),
                ('challenge_issued', models.DateTimeField(default=datetime.datetime(2020, 4, 7, 5, 7, 45, 439964), verbose_name='date issued')),
                ('challenge_message', models.TextField(default='Unknown')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='game_black',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_content',
            field=models.TextField(default='Unknown'),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 7, 5, 7, 45, 439964), verbose_name='date played'),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_result',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_round',
            field=models.CharField(default='1', max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_white',
            field=models.CharField(default='Unknown', max_length=200),
        ),
    ]