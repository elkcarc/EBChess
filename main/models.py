from django.db import models

# Create your models here.
class Game(models.Model):
    game_players = models.CharField(max_length=200)
    game_content = models.TextField()
    game_published = models.DateTimeField("date played")

    def __str__(self):
        return self.game_players