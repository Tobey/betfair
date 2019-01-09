import os

import json
from datetime import datetime
from pprint import pprint

import requests
import requests_cache

requests_cache.install_cache()


from django.core.management import BaseCommand
from bs4 import BeautifulSoup

from nba import models

path = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(path, 'teams.json')))


stats_mapping = {
    'wins': 'wins',
    'losses': 'losses',
    'winpercent': 'win_percent',
    'avgpointsfor': 'avg_points_for',
    'avgpointsagainst': 'avg_points_against',
    'streak': 'streak',
    'playoffseed': 'playoff_seed',
    'divisionwinpercent': 'division_win_percent',
    'leaguewinpercent': 'league_win_percentange',
    'threepoints': 'threepoints_or_less',
    'tenpoints': 'tenpoints_or_more',
    'vsorbetter': 'vsorbetter',
    'vsbelow': 'vsorbelow',
}




def get_player_details(url):
    slug = url.split('/')[-1]
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')

    img = soup.select_one('.main-headshot')
    img = img.find('img')['src'] if img else  None

    return dict(slug=slug, img=img)


def get_player_from_instance(instance):
    print(f'scraping {instance.website}')

    soup = BeautifulSoup(requests.get(instance.website).text, 'html5lib')

    roster = soup.select_one('.Table2__table-scroller.Table2__table')
    rows = roster.select('tr')
    for row in rows:
        columns = row.select('td')
        if not columns:
            continue

        name = columns[1].text.strip()
        url = columns[1].find('a').get('href')

        if url:
            print(f'Getting more data for {name}')
            more_dets = get_player_details(url)
            more_dets['img'] = more_dets['img'] or instance.logo
        else:
            more_dets = dict()

        no = columns[0].text.strip()
        pos = columns[2].text.strip()

        dets = dict(**more_dets, name=name, no=no, pos=pos, team=instance)
        player, _ = models.Player.objects.update_or_create(dets, slug=dets['slug'])


class Command(BaseCommand):

    def handle(self, *args, **options):
        for conference in data['children']:
            conf = conference['abbreviation'].lower()
            team_data = conference['standings']['entries']
            info = {}
            print('Making Teams...')

            for payload in team_data:
                info['conference'] = conf
                team = payload['team']
                print(team)
                stats = payload['stats']
                info['name'] = team['displayName']
                info['slug'] = team['abbreviation'].lower()
                info['logo'] = team['logos'][0]['href']

                for stat in stats:
                    if stat['type'] in stats_mapping:
                        info[stats_mapping[stat['type']]] = stat.get('value', stat['displayValue'])
                instance, _ = models.Team.objects.update_or_create(info, name=info['name'])

                get_player_from_instance(instance)
