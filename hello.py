from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/', methods=['GET', 'POST'])
def index():
    # Si la barre de recherche a été soumise
    if request.method == 'POST':
        query = request.form['query']
        # field = request.form['field']
        field = request.form.get('field')
        data = search(query, field)
        return render_template('hello.html', data=data)
    else:
        # Recherchez tous les documents dans l'index "yt_twitch"
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 1500)
        # Récupérez les documents et les stockez dans une liste
        data = [hit['_source'] for hit in result['hits']['hits']]
        return render_template('hello.html', data=data)

def search(query, field):
    QUERY ={
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "bool": {
                "should": [
                {
                    "match_phrase": {
                    field : query
                    }
                }
                ],
                "minimum_should_match": 1
            }
            }
        ],
        "should": [],
        "must_not": []
        }
    }
    }
    result = es.search(index="yt_twitch", body=QUERY,size=1500)

    results = []
    [results.append(elt['_source']) for elt in result["hits"]["hits"]]

    return results

if __name__ == '__main__':
    app.run(debug=True)
