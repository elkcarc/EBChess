from django.contrib import admin
from .models import Game
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Game ID", {"fields":["game_id"]}),
        ("Game Info", {"fields":["game_event", "game_site", "game_round"]}),
        ("Title/date", {"fields":["game_white", "game_black", "game_published"]}),
        ("Content", {"fields":["game_content", "game_result"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

admin.site.register(Game, GameAdmin)


