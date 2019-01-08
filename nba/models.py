from django.db import models
import requests


class Fixture(models.Model):
    date = models.DateField()

    _d = None

    @property
    def info(self):
        if not self._d:
            print('making requets....')
            self._d = self.api_data()

        return self._d

    def api_data(self):
        url = 'http://sportscenter.api.espn.com/apis/v2/events'

        params =  {
                 "advance": "true",
              "sport": "basketball",
              "league": "nba",
              "profile": "sportscenter_v1",
              "platform": "ios",
              "device": "handset",
              "lang": "en",
              "region": "gb",
              "dates": str(self).replace('-', ''),
              "timeOffset": "0",
              "supportedPackages": "ESPN_PLUS",
              "authorizedNetworks": "buzzerbeater,espn1,espn2,espn3,espnclassic,espndeportes,espnews,espnu,goalline,longhorn,sec",
              "hasMVPDAuthedEver": "false",
              "includeCalendar": "true",
              "version": "18",
              "appName": "espnapp",
              "locale": "GB",
              "isPremium": "false"
            }

        headers = {
            'Host': 'sportscenter.api.espn.com',
            'Accept': '*/*',
            'X-Personalization-Source': 'espnapp-ios-handset_en-gb',
            'AppVersion': '6.3.0',
            'X-ESPNAPP-Load-Type': 'initial',
            'Accept-Language': 'en-gb',
            'Accept-Encoding': 'gzip, deflate',
            'X-ESPNAPP-Clubhouse-UID': 's:40~l:46~section:scores',
            'User-Agent': 'ESPN/4225 CFNetwork/974.2.1 Darwin/18.0.0',
            'Cookie': 'SWID=A1108BF2-E330-4EAC-BBD5-56239136E8F5; DE2="Z2JyO2xuZDtsb25kb247eGRzbDs1OzU7NTs4MjYwNDQ7NTEuNTE0NzE7LTAuMDgzMjk7ODI2OzI1NDQ3OzQ3ODI7NTt1azs="; DS=YnQuY29tOzQ4MTMwMjticml0aXNoIHRlbGVjb21tdW5pY2F0aW9ucyBwbGM7',
            'Connection': 'keep-alive',
        }

        return requests.get(url, params=params, headers=headers).json()


    def __str__(self):
        return str(self.date)
