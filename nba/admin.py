from django.contrib import admin
from django.utils.html import format_html

from nba import models


class PlayerInline(admin.TabularInline):
    model = models.Player

    fields = (
        'thumbnail',
        'name',
        'pos',
        'no',
    )
    readonly_fields = fields
    extra = 0

    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.img}" height="50" width="50" />')


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'thumbnail',
        'wins',
        'losses',
        'win_percent',
        'avg_points_for',
        'streak',
    )

    fields = (
        ('name', 'slug', 'conference', 'thumbnail'),
        ('wins', 'losses'),
        ('win_percent', 'avg_points_for', 'avg_points_against', 'streak'),
        ('playoff_seed', 'division_win_percent', 'league_win_percentange'),
        ('threepoints_or_less', 'tenpoints_or_more', 'vsorbetter', 'vsorbelow'),
    )
    readonly_fields = (
        'thumbnail',
    )

    inlines = (
        PlayerInline,
    )
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.logo}" height="42" width="42" />')

