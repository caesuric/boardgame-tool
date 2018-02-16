import tornado.websocket
import tornado.escape
import random
import uuid

import data

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    tables = {}
    def open(self):
        SocketHandler.clients.append(self)
        self.player = None
        self.table = None
    def on_close(self):
        SocketHandler.clients.remove(self)
        self.table['players'].remove(self.player)
        for player in self.table['players']:
            player['handler'].update_table_players(self.table)
        if len(self.table['players'])==0:
            del SocketHandler.tables[self.table['name']]
    def on_message(self,message):
        parsed = tornado.escape.json_decode(message)
        lookup = {
            'queryGames': self.query_games,
            'queryGameSample': self.query_game_sample,
            'sendInBestGames': self.send_in_best_games,
            'createExplorerTable': self.create_explorer_table,
            'getTableInfo': self.get_table_info,
            'joinTable': self.join_table,
            'readyState': self.change_ready_state
        }
        lookup[parsed['message']](parsed)
    def query_games(self, message):
        data.DataHandler.data.sort(key=lambda x : x.rank)
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id} for x in data.DataHandler.data if x.min_players<int(message['players']) and x.max_players>int(message['players']) and x.max_time<=int( message['minutes'])]
        self.attempt_to_write_message({'message': 'gameList', 'games': games})
    def query_game_sample(self, message):
        data.DataHandler.data.sort(key=lambda x : x.num_owned, reverse=True)
        entries = []
        for i in range(int(len(data.DataHandler.data)/10)):
            entries.append(data.DataHandler.data[i])
        entries2 = []
        while len(entries2)<10:
            choice = random.choice(entries)
            if choice not in entries2 and choice.max_time<=self.table['minutes'] and choice.min_players <= len(self.table['players']) and choice.max_players >= len(self.table['players']):
                entries2.append(choice)
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id} for x in entries2]
        self.attempt_to_write_message({'message': 'gameList', 'games': games})
    def send_in_best_games(self, message):
        if not self.player:
            return
        if self.player['gamesSubmitted']:
            return
        for entry in message['games']:
            self.table['games'].append(entry)
        self.player['gamesSubmitted'] = True
        if self.check_if_all_games_submitted():
            calculate_best_games(self.table)
    def create_explorer_table(self, message):
        new_table = {'name': str(uuid.uuid4())[0:4], 'players': [], 'games': [], 'minutes': message['minutes']}
        new_table['players'].append(self.create_player(message['name']))
        SocketHandler.tables[new_table['name']] = new_table
        self.table = new_table
        self.attempt_to_write_message({'message': 'newTable', 'tableName': new_table['name']})
    def get_table_info(self, message):
        if 'table' not in message:
            return
        if message['table'] in SocketHandler.tables:
            table = SocketHandler.tables[message['table']]
            self.update_table_players(table)
    def join_table(self, message):
        if 'table' not in message:
            return
        if message['table'] in SocketHandler.tables:
            table = SocketHandler.tables[message['table']]
            player = self.create_player(message['name'])
            table['players'].append(player)
            self.table = table
            for person in table['players']:
                person['handler'].update_table_players(table)
    def change_ready_state(self, message):
        if self.player:
            self.player['ready'] = message['readyState']
            if self.check_if_table_ready():
                for player in self.table['players']:
                    player['handler'].table_ready()
    def check_if_table_ready(self):
        if not self.table:
            return False
        for player in self.table['players']:
            if not player['ready']:
                return False
        return True
    def check_if_all_games_submitted(self):
        if not self.table:
            return False
        for player in self.table['players']:
            if not player['gamesSubmitted']:
                return False
        return True
    def table_ready(self):
        self.attempt_to_write_message({'message': 'tableReady'})
    def create_player(self, name):
        player = {'handler': self, 'name': name, 'ready': False, 'gamesSubmitted': False}
        self.player = player
        return player
    def update_table_players(self, table):
        people = []
        you = ''
        for person in table['players']:
            people.append({'name': person['name']})
            if person['handler']==self:
                you = person['name']
        self.attempt_to_write_message({'message': 'tableInfo', 'players': people, 'you': you})
    def attempt_to_write_message(self, message):
        try:
            self.write_message(message)
        except Exception as e:
            print e
            print message[17]
            print 'CONNECTION LOST'

def calculate_best_games(table):
    data.DataHandler.data.sort(key=lambda x : x.rank)
    for entry in data.DataHandler.data:
        entry.value = 0
    selected_tags = {}
    for entry in find_games(table['games']):
        composite_list = []
        for mechanic in entry.mechanics:
            composite_list.append(mechanic)
        for category in entry.categories:
            composite_list.append(category)
        for designer in entry.designers:
            composite_list.append(designer)
        for tag in composite_list:
            if tag in selected_tags:
                selected_tags[tag] += 1
            else:
                selected_tags[tag] = 1
    for entry in data.DataHandler.data:
        for tag in selected_tags:
            if tag in entry.mechanics or tag in entry.categories or tag in entry.designers:
                entry.value += selected_tags[tag]
    data.DataHandler.data.sort(key=lambda x : x.value, reverse=True)
    result = []
    i = 0
    while len(result)<10:
        game = data.DataHandler.data[i]
        if game.max_time<=table['minutes'] and game.min_players <= len(table['players']) and game.max_players >= len(table['players']):
            result.append(data.DataHandler.data[i])
        i += 1
    games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id, 'algorithmScore': x.value} for x in result]
    why = sorted(selected_tags.iteritems(), key=lambda (k,v): (v,k))
    why.reverse()
    for player in table['players']:
        player['handler'].attempt_to_write_message({'message': 'gameList', 'games': games, 'why': why})
def find_games(ids):
    result = []
    for id_num in ids:
        for entry in data.DataHandler.data:
            if entry.id==id_num:
                result.append(entry)
                break
    return result
