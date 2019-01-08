from django.contrib import admin
from django.utils.html import format_html

from nba import models


@admin.register(models.Fixture)
class FixtureAdmin(admin.ModelAdmin):



    def data(self, obj):
        return obj.info

    def data3(self, obj):
        return obj.info

    def do(self, obj):
        fields = [
            'date',
        ]

        team_one = [[],[],[]]
        team_two= [[],[],[]]
        for i, data in enumerate(obj.info['content'][0]['items'], 1):
            team_one[0].append(data['teamOneName'])
            team_one[1].append(data['teamOneLogoURL'])
            team_one[2].append( data['teamOneScore'])

            team_two[0].append(data['teamTwoName'])
            team_two[1].append(data['teamTwoLogoURL'])
            team_two[2].append(data['teamTwoScore'])

            fields.append((f'match_{i}_team1', f'match_{i}_team1_logo', f'match_{i}_team1_score'))
            fields.append((f'match_{i}_team2', f'match_{i}_team2_logo', f'match_{i}_team2_score'))
            print(team_two, team_two)

            setattr(self, f'match_{i}_team1', lambda *a, **k: self.t1[0][i-1])
            setattr(self, f'match_{i}_team1_logo', lambda *a, **k: format_html(u'<img src="%s" height="42" width="42" />' % self.t1[1][i-1]))
            setattr(self, f'match_{i}_team1_score', lambda *a, **k: self.t1[2][i-1])
            setattr(self, f'match_{i}_team2', lambda *a, **k: self.t2[0][i-1])
            setattr(self, f'match_{i}_team2_logo', lambda *a, **k:format_html( u'<img src="%s" height="42" width="42" />' % self.t2[1][i-1]))
            setattr(self, f'match_{i}_team2_score', lambda *a, **k: self.t2[2][i-1])
            f = 2

        self.t1 = team_one
        self.t2 = team_two
        return fields

    def get_fields(self, request, obj=None):

        return self.do(obj)

    def get_readonly_fields(self, request, obj=None):
        d = []
        f  = self.do(obj)
        for t in f:
            if isinstance(t, str):
                d.append(t)
            else:
                for a in t:
                    d.append(a)
        return d


