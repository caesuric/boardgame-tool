import tornado.websocket
import tornado.escape
import random

import data

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
    def on_message(self,message):
        parsed = tornado.escape.json_decode(message)
        if parsed['message']=='queryGames':
            self.query_games(parsed)
        elif parsed['message']=='queryGameSample':
            self.query_game_sample(parsed)
        elif parsed['message']=='calculateBestGames':
            self.calculate_best_games(parsed)
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
        while len(entries2)<5:
            choice = random.choice(entries)
            if choice not in entries2:
                entries2.append(choice)
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id} for x in entries2]
        self.attempt_to_write_message({'message': 'gameList', 'games': games})
    def calculate_best_games(self, message):
        data.DataHandler.data.sort(key=lambda x : x.rank)
        for entry in data.DataHandler.data:
            entry.value = 0
        selected_mechanics = {}
        for entry in self.find_games(message['games']):
            for mechanic in entry.mechanics:
                if mechanic in selected_mechanics:
                    selected_mechanics[mechanic] += 1
                else:
                    selected_mechanics[mechanic] = 1
        for entry in data.DataHandler.data:
            for mechanic in selected_mechanics:
                if mechanic in entry.mechanics:
                    entry.value += selected_mechanics[mechanic]
        data.DataHandler.data.sort(key=lambda x : x.value, reverse=True)
        result = []
        for i in range(10):
            result.append(data.DataHandler.data[i])
        games = [{'name': x.name, 'bggUrl': x.bgg_url, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url, 'id': x.id} for x in result]
        self.attempt_to_write_message({'message': 'gameList', 'games': games})
    def find_games(self, ids):
        result = []
        for id_num in ids:
            for entry in data.DataHandler.data:
                if entry.id==id_num:
                    result.append(entry)
                    break
        return result
    def attempt_to_write_message(self, message):
        try:
            self.write_message(message)
        except Exception as e:
            print e
            print message[17]
            print 'CONNECTION LOST'
