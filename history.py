import json

class History(object):
    def __init__(self):
        with open('games.json') as data_file:
            self.games = json.load(data_file)

        with open('teams.json') as data_file:
            self.servers = json.load(data_file)

        self.history = []
        self.create_history()

    def create_history(self):
        for game in self.games:
            winner = self.get_team(game['winner']['name'])
            loser = self.get_team(game['loser']['name'])
            if winner and loser:
                game['winner']['players'] = winner.get('players')[:+4]
                game['loser']['players'] = loser.get('players')[:+4]
                del game['winner']['url']
                del game['loser']['url']

                game['winner']['composition'] = winner['composition']
                game['loser']['composition'] = loser['composition']

                self.history.append(game)
                

        with open('history.json', 'w') as outfile:
            json.dump(self.history, outfile)


    def get_team(self, team_name):
        server = self.get_server(team_name[:-2].replace('-', ' '))
        try:
            for team in server['teams']:
                if team['name'] == team_name:
                    return team
        except TypeError:
            pass

    def get_server(self, server_name):
        for server in self.servers:
            if server['name'] == server_name:
                return server




















            # for death in game['winner']['deaths']:
            #     if winner['players']['death']:
            #         winner['players']['death'] += 1
            #     else:
            #         winner['players']['death'] = 1

            # for death in game['loser']['deaths']:
            #     if loser['players']['death']:
            #         loser['players']['death'] += 1
            #     else:
            #         loser['players']['death'] = 1


history = History()