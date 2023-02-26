from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Integer
from elasticsearch.helpers import bulk
from flask import Flask, render_template, request

# Définition de fonctions

def generate_data(data):
    for docu in data:
        yield {
            "_index": "yt_twitch",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

# Initialiser le navigateur

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# Naviguer vers Twitch
driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")

time.sleep(5)

card= []

for i in range(2,22):
    card+= driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/section/div[4]/div/div[1]/div["+str(i)+"]")

features= [card[i].text.split("\n") for i in range(len(card))]

jeu= [features[i][0] if features[i][0]!="NOUVEAU" else features[i][1] for i in range(len(card))]
nb_spec= [features[i][1] if features[i][0]!="NOUVEAU" else features[i][2] for i in range(len(card))]
tags= [features[i][2:] if features[i][0]!="NOUVEAU" else features[i][3:] for i in range(len(card))]

data_twitch= pd.DataFrame(list(zip(jeu, nb_spec, tags)), columns=["Jeu", "Nombre de spectateurs", "Tags"]) #Dataframe final

presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located
wait = WebDriverWait(driver, 5)
data_youtube=pd.DataFrame()

for k in range(0,3):

    print(k)
    titre= []
    nb_vue= []
    date= []
    chaine= []
    jeu= []
    lien=[]
    titres= []
    nb_vues= []
    dates= []
    chaines= []
    jeux=[]
    liens=[]
    temp_df=[]

    # Navigate to url with video being appended to search_query
    driver.get('https://www.youtube.com/results?search_query={}'.format(str(data_twitch["Jeu"][k])))
    
    time.sleep(1)

    if k==0:
        button = driver.find_element(By.XPATH,"//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
        button.click()

    try:
        # code à tester
        driver.find_element(By.XPATH, "//*[@id='watch-card-subtitle']").click()
    except:
        # code à exécuter en cas d'exception
        continue

    wait.until(visible((By.XPATH, "//*[@id='tabsContent']/tp-yt-paper-tab[3]/div")))
    driver.find_element(By.XPATH, "//*[@id='tabsContent']/tp-yt-paper-tab[3]/div").click()

    time.sleep(2)

    height = driver.execute_script('''var body = document.body,
                                        html = document.documentElement;
                                        var height = Math.max( body.scrollHeight, body.offsetHeight, 
                                        html.clientHeight, html.scrollHeight, html.offsetHeight );
                                        return height;''')

    driver.execute_script("window.scrollTo(0, "+str(height)+");")

    # Extraire le nombre de spectateurs à partir de l'élément HTML approprié

    time.sleep(2)

    for i in range(1,101):
        
        titre+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/h3/a")
        chaine+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a")
        nb_vue+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/span[1]")
        date+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/span[2]")
        jeu+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-interactive-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div/div/div/div[1]")
        lien+= driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/h3/a")

    # Récupération des données des vidéos Youtube

    titres+=[titre[i].text for i in range(len(titre))]
    chaines+=[chaine[i].text for i in range(len(chaine))]
    nb_vues+=[nb_vue[i].text for i in range(len(nb_vue))]
    dates+=[date[i].text for i in range(len(date))] 
    jeux+=[jeu[i].text for i in range(len(jeu))]
    liens+=[lien[i].get_attribute('href') for i in range(len(lien))]
    temp_df= pd.DataFrame(list(zip(jeux,titres, chaines, nb_vues, dates, liens)))
    data_youtube= pd.concat([data_youtube,temp_df], axis=0)

driver.quit()

data_youtube.columns = ['Jeu', 'Titre', 'Chaîne', 'Nombre de vues', 'Date de la mise en ligne', 'Lien de la vidéo']

data_youtube['Nombre de vues'] = data_youtube['Nombre de vues'].apply(lambda x: int((x.replace('M', '000000').replace('k', '000').replace(',', '').replace('de vues', '').replace('vues', '').replace(' ', '').replace('spectateurs', ''))))

data = data_youtube.to_dict('records')

# Initilisation de Docker

es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])

if es.indices.exists(index='yt_twitch')==True:
    es.indices.delete(index='yt_twitch')
    bulk(es, generate_data(data))
else :
    bulk(es, generate_data(data))


###### FLASK #######

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)