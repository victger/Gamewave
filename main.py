from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask import Flask, render_template, request

# Définition de la fonction permettant d'utiliser les dataframes générés sur Elsstic Search

def generate_data(data):
    for docu in data:
        yield {
            "_index": "yt_twitch",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

# On initialise le navigateur pour scrapper

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

# Navigation vers Twitch

driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")

time.sleep(1)

# card correspond à l'ensemble des informations textuelles dans la carte de jeu

card= []

for i in range(2,22):
    card+= driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/section/div[4]/div/div[1]/div["+str(i)+"]")

# On récupère toutes les informations textuelles contenues dans les cartes en splittant le texte

features= [card[i].text.split("\n") for i in range(len(card))]

# On range les informations dans les tableaux adéquats en faisant attention à ne pas inclure l'information NOUVEAU qui nous est inutile

jeu= [features[i][0] if features[i][0]!="NOUVEAU" else features[i][1] for i in range(len(card))]
nb_spec= [features[i][1] if features[i][0]!="NOUVEAU" else features[i][2] for i in range(len(card))]
tags= [features[i][2:] if features[i][0]!="NOUVEAU" else features[i][3:] for i in range(len(card))]

# On range toutes les informations dans une dataframe

data_twitch= pd.DataFrame(list(zip(jeu, nb_spec, tags)), columns=["Jeu", "Nombre de spectateurs", "Tags"]) #Dataframe final

presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located
wait = WebDriverWait(driver, 5)
data_youtube=pd.DataFrame()

# Cette boucle permet de parcourir tous les jeux contenus dans notre dataframe Twitch sur Youtube. Il faut changer le paramètre len(data_twitch) pour echercher moins de jeux

for k in range(0,len(data_twitch)):

    # A chaque itération, on initialise nos tableaux pour concaténer nos informations dans la dataframe sans doublons

    titre= []
    nb_vue= []
    date= []
    chaine= []
    jeu= []
    lien=[]
    tag= []
    titres= []
    nb_vues= []
    dates= []
    chaines= []
    liens=[]
    temp_df=[]

    # Navigation vers le ième jeu de notre datafrme Twitch

    driver.get('https://www.youtube.com/results?search_query={}'.format(str(data_twitch["Jeu"][k])))
    
    time.sleep(1)

    # Acceptation des cookies Youtube à la première itération

    if k==0:
        button = driver.find_element(By.XPATH,"//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
        button.click()

    # On clique sur la carte de jeu Youtube si elle est disponible, sinon on passe à la prochaine itération.

    try:
        driver.find_element(By.XPATH, "//*[@id='watch-card-subtitle']").click()
    except:
        continue

    # On clique sur l'onglet "Récentes" dans la carte du jeu

    wait.until(visible((By.XPATH, "//*[@id='tabsContent']/tp-yt-paper-tab[3]/div")))
    driver.find_element(By.XPATH, "//*[@id='tabsContent']/tp-yt-paper-tab[3]/div").click()

    time.sleep(2)

    # On scrolle suffisamment dans la page pour scrapper 100 vidéos de la carte de jeu dans l'onglet "Récentes"

    height = driver.execute_script('''var body = document.body,
                                        html = document.documentElement;
                                        var height = Math.max( body.scrollHeight, body.offsetHeight, 
                                        html.clientHeight, html.scrollHeight, html.offsetHeight );
                                        return height;''')

    driver.execute_script("window.scrollTo(0, "+str(height)+");")

    time.sleep(2)

    # On récupère le titre, la chaîne, le nombre de vues, la date, le jeu ainsi que le lien de la vidéo concernée

    for i in range(1,101):
        
        titre+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/h3/a")
        chaine+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a")
        nb_vue+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/span[1]")
        date+=driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/span[2]")
        jeu.append(data_twitch['Jeu'][k])
        tag.append(data_twitch['Tags'][k])
        lien+= driver.find_elements(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer["+str(i)+"]/div[1]/div[1]/div[2]/div/h3/a")

    # On range les informations sous formes de textes dans des tableaux

    titres+=[titre[i].text for i in range(len(titre))]
    chaines+=[chaine[i].text for i in range(len(chaine))]
    nb_vues+=[nb_vue[i].text for i in range(len(nb_vue))]
    dates+=[date[i].text for i in range(len(date))]
    liens+=[lien[i].get_attribute('href') for i in range(len(lien))]

    # On crée une dataframe temporaire contenant les informations de la vidéo en cours de scraping et on concatène toutes les dataframes temporaires pour obtenir la dataframe finale.

    temp_df= pd.DataFrame(list(zip(jeu,titres, chaines, nb_vues, dates, tag, liens)))
    data_youtube= pd.concat([data_youtube,temp_df], axis=0)
driver.quit()

# On renomme correctement les colonnes et on effectue un foramttage de la colonne "Nombre de vues"

data_youtube.columns = ['Jeu', 'Titre', 'Chaîne', 'Nombre de vues', 'Date de la mise en ligne', 'Tags', 'Lien de la vidéo']
data_youtube['Nombre de vues'] = data_youtube['Nombre de vues'].apply(lambda x: int((x.replace('M', '000000').replace('k', '000').replace(',', '').replace('de vues', '').replace('vues', '').replace(' ', '').replace('spectateurs', ''))))
print(data_youtube)

data = data_youtube.to_dict('records') # On transforme la dataframe en dictionnaire pour l'inclure dans Docker

# Initilisation de Docker

es = Elasticsearch([{'host': 'localhost', 'port': 9200,"scheme": "http"}])

if es.indices.exists(index='yt_twitch')==True:
    es.indices.delete(index='yt_twitch')
    bulk(es, generate_data(data))
else :
    bulk(es, generate_data(data))


# ###### FLASK #######

app = Flask(__name__)

# Page d'accueil -> On répertorie toutes les informations de notre dataframe

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        result = es.search(index="yt_twitch", body={"query": {"match_all": {}}},size = 2000)
        data = [hit['_source'] for hit in result['hits']['hits']]
        return render_template('index.html', data=data)

# Création d'une nouvelle page recherche dans laquelle on effectue une recherche sur les jeux avec une sélection

@app.route('/filtrage_jeu', methods=['GET', 'POST'])
def filtrage_jeu():
    if request.method == 'GET':
        jeu = request.args.get('jeu')
        filtre_jeux = search2(jeu)
        data = [hit['_source'] for hit in filtre_jeux['hits']['hits']]
        return render_template('index.html', data=data)

# Création d'une nouvelle page recherche dans laquelle on effectue une recherche sur les mots

@app.route('/filtrage_mots', methods=['GET', 'POST'])
def filtrage_mots():
    if request.method == 'GET':
        query = request.args.get('query')
        fields = request.args.get('fields')
        fields= fields.split('|')
        data = search(query, fields)
        return render_template('index.html', data=data)

# Requête search faisaint une recherche sur les mots donnés dans la barre de recherche

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

# Requête search2 faisant une recherche sur les jeux de la sélection

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

app.run()