from flask import Flask, render_template, request
from flask_cors import CORS
from app.elastic import *

app = Flask(__name__)
CORS(app)

# Page d'accueil -> On répertorie toutes les informations de notre dataframe

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 2000)
        data = [hit['_source'] for hit in result['hits']['hits']]
        return render_template('index.html', data=data)
    
@app.route('/search')
def search_autocomplete():
    query = request.args["q"].lower()
    tokens = query.split(" ")

    clauses = [
        {
            "span_multi": {
                "match": {"fuzzy": {"Game": {"value": i, "fuzziness": "AUTO"}}}
            }
        }
        for i in tokens
    ]

    payload = {
        "bool": {
            "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
        }
    }

    response= es.search(index="yt_twitch", query=payload, size=100)

    game_suggestions= list(set([result['_source']['Game'] for result in response['hits']['hits']]))

    return game_suggestions