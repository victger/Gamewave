from flask import Flask, render_template, url_for, request, session, redirect
from es_code import Video
from elasticsearch_dsl import Search

app = Flask(__name__)

@app.route('/')
def index():
    results = Video.search().execute()
    return render_template('hello.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)