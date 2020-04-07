from django.contrib import admin
from .models import Game, Challenge, Active, Ai
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('game_id',)
    fieldsets = [
        ("Game Info", {"fields":["game_event", "game_site", "game_round"]}),
        ("Title/date", {"fields":["game_white", "game_black", "game_published"]}),
        ("Content", {"fields":["game_content", "game_result"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

    def game_id(self, obj):
        return obj.id

class ChallengeAdmin(admin.ModelAdmin):
    readonly_fields = ('challenge_id',)
    fieldsets = [
        ("Title/date", {"fields":["challenge_user1", "challenge_user2", "challenge_issued"]}),
        ("Content", {"fields":["challenge_message"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

    def challenge_id(self, obj):
        return obj.id

class ActiveAdmin(admin.ModelAdmin):
    readonly_fields = ('active_id',)
    fieldsets = [
        ("Title/date", {"fields":["user1", "user2", "last_move"]}),
        ("Content", {"fields":["active_content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

    def active_id(self, obj):
        return obj.id

class AiAdmin(admin.ModelAdmin):
    readonly_fields = ('ai_id',)
    fieldsets = [
        ("Title/date", {"fields":["user", "user_side", "last_move"]}),
        ("Content", {"fields":["ai_content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }

    def ai_id(self, obj):
        return obj.id

admin.site.register(Game, GameAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Active, ActiveAdmin)
admin.site.register(Ai, AiAdmin)

