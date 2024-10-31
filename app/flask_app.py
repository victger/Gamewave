from flask import Flask, render_template, request
from app.elastic import *

app = Flask(__name__)

# Page d'accueil -> On répertorie toutes les informations de notre dataframe

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 2000)
        data = [hit['_source'] for hit in result['hits']['hits']]
        return render_template('index.html', data=data)

# Création d'une nouvelle page recherche dans laquelle on effectue une recherche sur les jeux avec une sélection

@app.route('/filter_game', methods=['GET', 'POST'])
def filter_game():
    if request.method == 'GET':
        game = request.args.get('game')
        filter_games = search2(game)
        data = [hit['_source'] for hit in filter_games['hits']['hits']]
        return render_template('index.html', data=data)

# Création d'une nouvelle page recherche dans laquelle on effectue une recherche sur les mots

@app.route('/filter_words', methods=['GET', 'POST'])
def filter_words():
    if request.method == 'GET':
        query = request.args.get('query')
        fields = request.args.get('fields')
        fields= fields.split('|')
        data = search(query, fields)
        return render_template('index.html', data=data)