# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
import json


class OfficialSpider(CrawlSpider):
    name = 'official'
    start_urls = [
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-01#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-03#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-05#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-08#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-10#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-11#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-12#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-13#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-14#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-15#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-16#jt_list/',
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-17#jt_list/',
        # 'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-18#jt_list/',
    ]


    def parse(self, response):
        with open('allgames.json') as data_file:
            games = json.load(data_file)
            done_id = self.extract_done_id(games)

            for href in response.css('table.ak-ladder tr td:last-child a::attr(href)'):
                done = False
                if self.make_url(href.extract())[-4:] in done_id:
                    done = True
                
                if not done:                        
                    url_object = response.urljoin(self.make_url(href.extract()))
                    yield scrapy.Request(url_object, callback=self.parse_combat_result_page)

    def extract_done_id(self, games):
        done_id = [game['id'] for game in games]
        return done_id

    def parse_combat_result_page(self, response):
        teams = self.get_teams(response)
        result = self.get_result(response)

        winner_result = result['teams'][teams['winner']['name']]
        teams['winner']['points'] = winner_result['points']
        teams['winner']['deaths'] = winner_result['deaths']
        loser_result = result['teams'][teams['loser']['name']]
        teams['loser']['points'] = loser_result['points']
        teams['loser']['deaths'] = loser_result['deaths']


        yield {
            'id': self.get_id(response),
            'winner': teams['winner'],
            'loser': teams['loser'],
            'turns': result['turns'],
        }


    def get_result(self, response):
        container = response.css('.row.ak-container')
        result = {}
        result['turns'] = container.css('div:first-child div:first-child strong::text').extract_first().strip()
        teams = {}
        for team_container in container.css('.ak-column.ak-container.col-md-6'):

            team_name = team_container.css('.ak-team-match-result strong::text').extract_first().lower().strip()
            teams[team_name] = {}

            teams[team_name]['points'] = team_container.css('.ak-team-match-result-points::text').extract_first()[+28:].strip()
            team_death = []

            for player in team_container.css('.ak-team-match-result-players .ak-panel-content .ak-list-element'):
                name = player.css('.ak-content .ak-title a::text').extract_first()
                dead = player.css('.ak-character-dead').extract_first()

                if dead:
                    team_death.append(name)

            teams[team_name]['deaths'] = team_death
        result['teams'] = teams
        return result

    def get_teams(self, response):
        teams = {}
        winner_name = self.get_winner_name(response).lower()

        for td in response.css('table.ak-ladder tbody tr td:first-child'):
            names = td.css('a::text').extract()
            urls = td.css('a::attr(href)').extract()
            winner = {}
            loser = {}

            for i in [0,1]:

                if names[i].lower() == winner_name:
                    winner['name'] = names[i].lower()
                    winner['url'] = self.make_url(urls[i])

                else:
                    loser['name'] = names[i].lower()
                    loser['url'] = self.make_url(urls[i])

                teams['winner'] = winner
                teams['loser'] = loser

        return teams 

    def get_winner_name(self, response):
        return response.css('table.ak-ladder tbody tr td:last-child a::text').extract_first()

    def get_id(self, response):
        return response.url.split("/")[-1]

    def make_url(self, url):
        return 'http://www.dofus.com{}'.format(url)



