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
    
from urllib.parse import parse_qs, urlparse

@app.route('/autocompletion')
def autocomplete():

    url = request.headers.get("Referer")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    current_game = query_params.get('game', [None])[0]
    current_video_title = query_params.get('video_title', [None])[0]
    current_channel = query_params.get('channel', [None])[0]
    current_date_range = query_params.get('date', [None])[0]
    current_tags = query_params.get('tags', [None])[0]

    field = request.args.get('field')
    query = request.args.get("q").lower()
    tokens = query.split(" ")

    query_body = {
        "bool": {
            "must": []
        }
    }

    if current_game:
        query_body["bool"]["must"].append({"match": {"Game": current_game}})
    if current_video_title:
        query_body["bool"]["must"].append({"match": {"Video title": current_video_title}})
    if current_channel:
        query_body["bool"]["must"].append({"match": {"Channel": current_channel}})
    if current_date_range:
        start_date, end_date = current_date_range.split(' - ')
        query_body["bool"]["must"].append({
            "range": {
                "Date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })
    if current_tags:
        query_body["bool"]["must"].append({"match": {"Tags": current_tags}})

    autocomplete_clauses = [
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

    query_body["bool"]["must"].extend(autocomplete_clauses)

    response = es.search(index="yt_twitch", query=query_body, size=2000)

    if field == "Tags":
        all_tags = []
        for result in response['hits']['hits']:
            tags = result['_source'][field]
            for tag in tags:
                clean_tag = tag.strip().lower()
                if any(token in clean_tag for token in tokens):
                    all_tags.append(tag)
        suggestions = list(set(all_tags))
    else:
        suggestions = list(set([result['_source'][field] for result in response['hits']['hits']]))

    return suggestions

@app.route('/search')
def search():
    game = request.args.get('game')
    video_title = request.args.get('video_title')
    channel = request.args.get('channel')
    date_range = request.args.get('date')
    tags = request.args.get('tags')

    query = {
        "bool": {
            "must": []
        }
    }

    if game:
        query["bool"]["must"].append({"match": {"Game": game}})
    
    if video_title:
        query["bool"]["must"].append({"match_phrase": {"Video title": video_title}})
    
    if channel:
        query["bool"]["must"].append({"match": {"Channel": channel}})
    
    if date_range:
        start_date, end_date = date_range.split(' - ')
        query["bool"]["must"].append({
            "range": {
                "Date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })
    
    if tags:
        query["bool"]["must"].append({"match": {"Tags": tags}})

    response = es.search(index="yt_twitch", query=query, size=2000)

    print(response)
    data = [hit['_source'] for hit in response['hits']['hits']]

    return render_template('index.html', data=data)