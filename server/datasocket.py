import tornado.websocket
import tornado.escape
import random
import uuid

import data

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    tables = []
    def open(self):
        SocketHandler.clients.append(self)
    def on_message(self,message):
        parsed = tornado.escape.json_decode(message)
        if parsed['message']=='queryGames':
            self.query_games(parsed)
        elif parsed['message']=='queryGameSample':
            self.query_game_sample(parsed)
        elif parsed['message']=='calculateBestGames':
            self.calculate_best_games(parsed)
        elif parsed['message']=='createExplorerTable':
            self.create_explorer_table(parsed)
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
            if choice not in entries2:
                entries2.append(choice)
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id} for x in entries2]
        self.attempt_to_write_message({'message': 'gameList', 'games': games})
    def calculate_best_games(self, message):
        data.DataHandler.data.sort(key=lambda x : x.rank)
        for entry in data.DataHandler.data:
            entry.value = 0
        selected_tags = {}
        for entry in self.find_games(message['games']):
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
        for i in range(10):
            result.append(data.DataHandler.data[i])
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id, 'algorithmScore': x.value} for x in result]
        why = sorted(selected_tags.iteritems(), key=lambda (k,v): (v,k))
        why.reverse()
        self.attempt_to_write_message({'message': 'gameList', 'games': games, 'why': why})
    def find_games(self, ids):
        result = []
        for id_num in ids:
            for entry in data.DataHandler.data:
                if entry.id==id_num:
                    result.append(entry)
                    break
        return result
    def create_explorer_table(self, message):
        new_table = {'name': uuid.uuid4()[0:4], 'people': []}
        new_table['people'].append(self)
        SocketHandler.tables.append(new_table)
        self.attempt_to_write_message({'message': 'newTable', 'tableName': new_table['name']})
    def attempt_to_write_message(self, message):
        try:
            self.write_message(message)
        except Exception as e:
            print e
            print message[17]
            print 'CONNECTION LOST'
