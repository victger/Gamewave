from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text, Integer
from elasticsearch_dsl.connections import connections
import pandas as pd

es = Elasticsearch([{"host":"localhost","port":9200}])
connections.create_connection(hosts=['localhost'], timeout=20)


# Définition du Document Elasticsearch
class Video(Document):
    title = Text()
    channel = Text()
    views = Text()
    date = Text()

    class Index:
        name = 'video_index'

# Créer l'index dans Elasticsearch s'il n'existe pas
Video.init()

# Charger la dataframe Pandas
df = pd.DataFrame({0: ['Hogwarts Legacy - Official Launch Trailer 4K', 'Hogwarts Legacy Review', "oueoue"],
                1: ['Hogwarts Legacy', 'IGN', 'gameranx'],
                2: ['3,2 M de vues', '1,8 M de vues', '1,8 M de vues'],
                3: ['il y a 6 jours', 'il y a 2 jours', 'il y a 1 jour']})
df.columns = ['title', 'channel', 'views', 'date']

# Convertir la dataframe en objets Video
objs = [Video(title=row['title'], channel=row['channel'], views=row['views'], date=row['date'])
        for idx, row in df.iterrows()]

# Insérer les objets dans Elasticsearch
for obj in objs:
    obj.save()

# results = Video.search().execute()
# for result in results:
#     print(result.title, result.channel, result.views, result.date)
