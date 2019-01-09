import json
from datetime import date

from django.core.management import BaseCommand

from nba import models


def schedule(instance):
    data = instance.api_data()
    items = data['content'][0]['items']
    for item in items:
        team_one = item['teamOneAbbreviation'].lower()
        team_two = item['teamTwoAbbreviation'].lower()

        team_one_score = item.get('teamOneScore') and int(item['teamOneScore'])
        team_two_score = item.get('teamTwoScore') and int(item['teamTwoScore'])

        lookup = dict(
            home_team=models.Team.objects.get(slug=team_one),
            away_team=models.Team.objects.get(slug=team_two),
            fixture=instance
        )

        defaults = dict(
            **lookup,
            home_score=team_one_score,
            away_score=team_two_score,
        )
        game_inst, _ = models.Game.objects.update_or_create(defaults, **lookup)


class Command(BaseCommand):

    def handle(self, *args, **options):

        today = date.today()
        fix = dict(date=today)
        instance, _ = models.Fixture.objects.update_or_create(fix, **fix)

        schedule(instance)










