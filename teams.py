# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
import json
import re


class OfficialSpider(CrawlSpider):
    name = 'official'
    start_urls = []

    def __init__(self):
        self.servers = {}
        self.done_teams = []
        self.done_servers = []

    def start_requests(self):
        with open('newteams.json') as data_file:
            servers = json.load(data_file)
            for server in servers:
                self.done_servers.append(server['name'])
                for team in server['teams']:
                    self.done_teams.append(team['name'])
                # print(self.done_teams)

        with open('games.json') as data_file:
            games = json.load(data_file)
            for game in games:
                print(game['winner']['name'].lower())
                if game['winner']['name'].lower()[:-2] not in self.done_servers and game['winner']['name'].lower() not in self.done_teams:
                    yield Request(game['winner']['url'], callback=self.parse)
                if game['loser']['name'].lower()[:-2] not in self.done_servers and game['loser']['name'].lower() not in self.done_teams:
                    yield Request(game['loser']['url'], callback=self.parse)

    def parse(self, response):
        yield self.create_servers(response)
        
    def create_servers(self, response):
        team = {}

        team['name'] = re.sub('-', ' ', response.url.split('/')[-1][+5:])
        team['server'] = team['name'][:-2]

        self.get_players_and_composition(response, team)
        
        if team['server'] not in self.servers:
            self.create_server(team)

        else:
            return self.append_team(team)

    def create_server(self, team):
        server = {
            'name': team['server'],
            'teams': [
                team
            ]
        }
        self.servers[server['name']] = server

    def append_team(self, team):
        server_teams = self.servers[team['server']]['teams']
        if team not in server_teams:
            server_teams.append(team)

        if len(server_teams) == 4:
            return self.return_server(team)

    def return_server(self, team):
        server = self.servers[team['server']]
        for team in server['teams']:
            self.done_teams.append(team['name'])
        del self.servers[team['server']]
        for team in server['teams']:
            self.done_teams.append(team['name'])
        return server

    def get_players_and_composition(self, response, team):
        team['composition'] = []
        team['players'] = []
        i = 0
        for container in response.css('.ak-panel-content'):
            i += 1
            if i == 4:
                for div in container.css('.ak-list-element .ak-content'):
                    name = div.css('.ak-title a strong::text').extract_first()
                    if name:
                        pass

                    classe = div.css('.ak-text::text').extract_first().partition(' ')[0]

                    if classe not in team['composition']:
                        team['composition'].append(classe)

                    player = {'name': name, 'classe': classe}
                    team['players'].append(player)

        return team

