from flask import Flask, render_template, request
from urllib.parse import parse_qs, urlparse
from flask_cors import CORS
from app.elastic import search_all_data, search_with_filters, autocomplete_suggestions

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = search_all_data("yt_twitch")
    return render_template('index.html', data=data)

@app.route('/autocompletion')
def autocomplete():
    url = request.headers.get("Referer")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    current_game = query_params.get('Game', [None])[0]
    current_video_title = query_params.get('Video title', [None])[0]
    current_channel = query_params.get('Channel', [None])[0]
    current_date_range = query_params.get('Date', [None])[0]
    current_tags = query_params.get('Tags', [None])[0]

    field = request.args.get('field')
    query = request.args.get("q").lower()
    tokens = query.split(" ")

    filters = []
    if current_game:
        filters.append({"match": {"Game": current_game}})
    if current_video_title:
        filters.append({"match": {"Video title": current_video_title}})
    if current_channel:
        filters.append({"match": {"Channel": current_channel}})
    if current_date_range:
        start_date, end_date = current_date_range.split(' - ')
        filters.append({"range": {"Date": {"gte": start_date, "lte": end_date}}})
    if current_tags:
        filters.append({"match": {"Tags": current_tags}})

    response = autocomplete_suggestions("yt_twitch", field, tokens, filters)

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
    game = request.args.get('Game')
    video_title = request.args.get('Video title')
    channel = request.args.get('Channel')
    date_range = request.args.get('Date')
    tags = request.args.get('Tags')

    filters = []
    if game:
        filters.append({"match": {"Game": game}})
    if video_title:
        filters.append({"match_phrase": {"Video title": video_title}})
    if channel:
        filters.append({"match": {"Channel": channel}})
    if date_range:
        start_date, end_date = date_range.split(' - ')
        filters.append({"range": {"Date": {"gte": start_date, "lte": end_date}}})
    if tags:
        filters.append({"match": {"Tags": tags}})

    data = search_with_filters("yt_twitch", filters)
    
    return render_template('index.html', data=data)