from flask import Flask, render_template, request
from flask_cors import CORS
from app.elastic import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 2000)
        data = [hit['_source'] for hit in result['hits']['hits']]
        return render_template('index.html', data=data)
    
    
@app.route('/search')
def search_autocomplete():
    field = request.args.get('field')
    query = request.args.get("q").lower()

    tokens = query.split(" ")

    clauses = [
        {
            "bool": {
                "should": [
                    {
                        "prefix": {
                            field: {
                                "value": i
                            }
                        }
                    },
                    {
                        "fuzzy": {
                            field: {
                                "value": i,
                                "fuzziness": "AUTO"
                            }
                        }
                    }
                ]
            }
        }
        for i in tokens
    ]

    payload = {
        "bool": {
            "must": clauses
        }
    }

    response = es.search(index="yt_twitch", query=payload, size=100)

    suggestions = list(set([result['_source'][field] for result in response['hits']['hits']]))

    return suggestions