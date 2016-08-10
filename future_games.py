# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scraper.items import MatchItem as Match
import json


class FutureSpider(CrawlSpider):
    name = 'future'
    start_urls = [
        'http://www.dofus.com/fr/mmorpg/communaute/tournois/goultarminator/calendrier?date=2016-08-10#jt_list/',
    ]


    def parse(self, response):
        self.games = []
        game = []
        for team in response.css('table.ak-ladder tr td:first-child a::text').extract():
            # team_with_composition = [team, composition]
            if len(game) == 0:
                game = [team]
            else:
                game.append(team)    
                self.games.append(game)
                game = []
        games_with_composition = []
        for game in self.games:
            i = 0

            teams_with_composition = []
            for team in game:
                i = i + 1
                team_with_composition = [str(team), self.get_team_composition(team)]
                teams_with_composition.append(team_with_composition)
                if i == 2:
                    i = 0
                    games_with_composition.append(teams_with_composition)


        print(games_with_composition)
        yield {
            'games': games_with_composition
        }

    def get_team_composition(self, team_name):
        with open('teams.json') as data_file:
            servers = json.load(data_file)
            for server in servers:
                for team in server['teams']:
                    if team['name'] == team_name.lower():
                        return team.get('composition')