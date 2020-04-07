from django.db import models
from datetime import datetime

# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=200)
    game_event = models.CharField(max_length=200)
    game_site = models.CharField(max_length=200)
    game_published = models.DateTimeField("date played", default=datetime.now())
    game_round = models.CharField(max_length=20)
    game_white = models.CharField(max_length=200)
    game_black = models.CharField(max_length=200)
    game_result = models.CharField(max_length=20)
    game_content = models.TextField()

    def __str__(self):
        return self.game_id