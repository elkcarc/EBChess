from django.contrib import admin
from .models import Game
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {"fields":["game_players", "game_published"]}),
        ("Content", {"fields":["game_content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

admin.site.register(Game, GameAdmin)


