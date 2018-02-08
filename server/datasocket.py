import tornado.websocket
import tornado.escape

import data

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass
    def on_message(self,message):
        parsed = tornado.escape.json_decode(message)
        if parsed['message']=='queryGames':
            self.query_games(parsed)
    def query_games(self, message):
        games = [{'name': x.name, 'rank': x.rank, 'minPlayers': x.min_players, 'maxPlayers': x.max_players, 'minTime': x.min_time, 'maxTime': x.max_time, 'imageUrl': x.image_url} for x in data.DataHandler.data if x.min_players<int(message['players']) and x.max_players>int(message['players']) and x.max_time<=int( message['minutes'])]
        self.attempt_to_write_message(unicode(tornado.escape.json_encode({'message': 'gameList', 'games': games}), errors='ignore'))
    def attempt_to_write_message(self, message):
        try:
            self.write_message(message)
        except Exception as e:
            print e
            print message[17]
            print 'CONNECTION LOST'
