from elasticsearch.helpers import bulk

def generate_data(data):
    for docu in data:
        yield {
            "_index": "yt_twitch",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

def insert_data(es,data):
    if es.indices.exists(index='yt_twitch')==True:
        es.indices.delete(index='yt_twitch')
        bulk(es, generate_data(data))
    else :
        bulk(es, generate_data(data))