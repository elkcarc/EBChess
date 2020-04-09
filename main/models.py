from django.db import models
from datetime import datetime

# Create your models here.
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_event = models.CharField(max_length=200, default="No Event")
    game_site = models.CharField(max_length=200, default="On-line")
    game_published = models.DateTimeField("date played", default=datetime.now())
    game_round = models.CharField(max_length=20, default="1")
    game_white = models.CharField(max_length=200, default="Unknown")
    game_black = models.CharField(max_length=200, default="Unknown")
    game_result = models.CharField(max_length=20, default="Unknown")
    game_content = models.TextField(default="None")
    game_fen = models.TextField(default="None")

    def __str__(self):
        return str(self.game_white + " vs " + self.game_black)

class Challenge(models.Model):
    challenge_id = models.AutoField(primary_key=True)
    challenge_user1 = models.CharField(max_length=200, default="Not Set")
    challenge_user2 = models.CharField(max_length=200, default="Not Set")
    challenge_issued = models.DateTimeField("date issued", default=datetime.now())
    challenge_message  = models.TextField(default="Unknown")

    def __str__(self):
        return str(self.challenge_user1 + " vs " + self.challenge_user2)

class Active(models.Model):
    active_id = models.AutoField(primary_key=True)
    user1 = models.CharField(max_length=200, default="Not Set")
    user2 = models.CharField(max_length=200, default="Not Set")
    last_move = models.DateTimeField("last move", default=datetime.now())
    active_content = models.TextField(default="None")
    active_fen = models.TextField(default="None")

    def __str__(self):
        return str(self.user1 + " vs " + self.user2)

class Ai(models.Model):
    ai_game_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=200, default="Not Set")
    user_side = models.CharField(max_length=10, default="White")
    last_move = models.DateTimeField("last move", default=datetime.now())
    ai_content = models.TextField(default="")