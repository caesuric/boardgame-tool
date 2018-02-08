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
                data_item = DataEntry(line[0], line[3], line[4], line[5], line[7], line[8], line[15], line[17], line[13])
                if (data_item.min_time>0 and data_item.max_time>0):
                    DataHandler.data.append(data_item)

class DataEntry:
    def __init__(self, rank, name, min_players, max_players, min_time, max_time, mechanics, categories, image_url):
        self.rank = int(rank)
        self.name = unicode(name, errors='ignore')
        self.min_players = int(min_players)
        self.max_players = int(max_players)
        self.min_time = int(min_time)
        self.max_time = int(max_time)
        self.mechanics = mechanics.split(', ')
        self.categories = categories.split(', ')
        self.image_url = unicode(image_url, errors='ignore')
