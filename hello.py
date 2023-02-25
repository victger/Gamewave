from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/', methods=['GET', 'POST'])
def index():
    # Recherchez tous les documents dans l'index "yt_twitch"
    result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 1500)
    # Récupérez les documents et les stockez dans une liste
    data = [hit['_source'] for hit in result['hits']['hits']]
    return render_template('hello.html', data=data)



    

if __name__ == '__main__':
    app.run(debug=True)
