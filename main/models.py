from django.db import models
from datetime import datetime

# Create your models here.
class Game(models.Model):
    game_players = models.CharField(max_length=200)
    game_published = models.DateTimeField("date played", default=datetime.now())
    game_content = models.TextField()

    def __str__(self):
        return self.game_players