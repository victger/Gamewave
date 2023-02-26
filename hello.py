from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 2000)
        data = [hit['_source'] for hit in result['hits']['hits']]
        # sort_order = request.args.get('asc')
        # print(sort_order)
        # data = sort_search_results(data, sort_order)
        return render_template('hello.html', data=data)
    
@app.route('/recherche', methods=['GET', 'POST'])
def recherche():
    if request.method == 'GET':
        jeu = request.args.get('jeu')
        filtre_jeux = search2(jeu)
        data = [hit['_source'] for hit in filtre_jeux['hits']['hits']]
        # sort_order = request.args.get('sort')
        # data = sort_search_results(data, sort_order)
        return render_template('hello.html', data=data)

@app.route('/filtrage_mots', methods=['GET', 'POST'])
def filtrage():
    if request.method == 'GET':
        query = request.args.get('query')
        fields = request.args.get('fields')
        fields= fields.split('|')
        data = search(query, fields)
        # sort_order = request.args.get('sort')
        # data = sort_search_results(data, sort_order)
        return render_template('hello.html', data=data)

def search(query, fields):
    QUERY ={
    "query": {
        "bool": {
        "must": [],
        "filter": [
            {
            "bool": {
                "should": [
                {
                    "multi_match": {
                        "query": query,
                        "fields": fields
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

def search2(menu_deroulant):
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
                    "Jeu" : menu_deroulant
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

    return result

# def sort_search_results(results, sort_order):
#     sorted_results = sorted(results, key=lambda x: x["Nombre de vues"], reverse=sort_order == "asc")
#     return sorted_results

if __name__ == '__main__':
    app.run(debug=True)
