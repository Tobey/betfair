from django.contrib import admin
from django.utils.html import format_html

from nba import models
from nba.management.commands.makefixture import schedule


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


class GameInline(admin.TabularInline):
    model = models.Game

    fields = (
        'home_team',
        'home_logo',
        'home_score',
        'away_team',
        'away_logo',
        'away_score',
    )

    readonly_fields = fields
    extra = 0

    def home_logo(self, obj):
        return format_html(f'<img src="{obj.home_team.logo}" height="50" width="50" />')

    def away_logo(self, obj):
        return format_html(f'<img src="{obj.away_team.logo}" height="50" width="50" />')


@admin.register(models.Fixture)
class FixtureAdmin(admin.ModelAdmin):

    inlines = (
        GameInline,
    )

    list_display = (
        'date',
        'table',
    )

    actions = [
        'get_fixture_schedule'
    ]

    def table(self, obj):
        data = ''
        for game in obj.games.all():
            data += f'<tr><td>{game.home_team}</th><th>{game.home_score}</td>' \
                    f'<td>{game.away_team}</th><th>{game.away_score}</td></tr>'

        table = f'''
        <table>
          <thead>
            <th>Home</th><th>Score</th><th>Away</th><th>Score</th>
          </thead>
          <tbody>
            {data}
          </tbody>
        </table>
        '''
        return format_html(table)

    def save_model(self, request, obj, form, change):
        ret = super().save_model(request, obj, form, change)
        schedule(obj)
        return ret

    def get_fixture_schedule(self, request, queryset):
        for fixture in queryset:
            schedule(fixture)
