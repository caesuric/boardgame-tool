import csv

def process():
    data_handler = DataHandler()

class DataHandler:
    data = []
    def __init__(self):
        with open('bgg_db_2017_04.csv', 'r') as raw_data:
            csv_reader = csv.reader(raw_data)
            counter = 0
            for line in csv_reader:
                counter += 1
                if counter==1:
                    continue
                data_item = DataEntry(line[0], line[1], line[3], line[4], line[5], line[7], line[8], line[15], line[17], line[13], line[16], line[2], line[18])
                if (data_item.min_time>0 and data_item.max_time>0):
                    DataHandler.data.append(data_item)

class DataEntry:
    def __init__(self, rank, bgg_url, name, min_players, max_players, min_time, max_time, mechanics, categories, image_url, num_owned, game_id, designers):
        self.rank = int(rank)
        self.name = unicode(name, errors='ignore')
        self.min_players = int(min_players)
        self.max_players = int(max_players)
        self.min_time = int(min_time)
        self.max_time = int(max_time)
        self.mechanics = unicode(mechanics, errors='ignore').split(', ')
        self.categories = unicode(categories, errors='ignore').split(', ')
        self.designers = unicode(designers, errors='ignore').split(', ')
        self.image_url = unicode(image_url, errors='ignore')
        self.bgg_url = unicode(bgg_url, errors='ignore')
        self.num_owned = int(num_owned)
        self.id = int(game_id)
