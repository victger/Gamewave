from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask import Flask, render_template, request
import sys

# Définition de la fonction permettant d'utiliser les dataframes générés sur Elastic Search

def generate_data(data):
    for docu in data:
        yield {
            "_index": "yt_twitch",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

# On initialise le navigateur pour scrapper

chrome_driver_path= r"C:\Users\vgvic\Documents\Projets\Trend_YT_Twitch\chromedriver-win64\chromedriver.exe"

driver = webdriver.Chrome(service=ChromeService(chrome_driver_path))
driver.maximize_window()

# Navigation vers Twitch

driver.get("https://www.twitch.tv/directory?sort=VIEWER_COUNT")
time.sleep(1)

# card correspond à l'ensemble des informations textuelles dans la carte de jeu

game_title= []
viewers= []
tags= []

for i in range(0, 10):  # Remplacer 10 par le nombre maximum de cartes que tu souhaites scraper
    try:
        # Attendre que l'élément avec un style 'order: i;' soit présent
        card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@style, 'order: {i};') and not(@id='directory-rectangle')]"))
        )

        # Extraire le titre du jeu
        game_title.append(card.find_element(By.XPATH, f"//a[contains(@data-a-target, 'card-{i}')]//h2").text)
        
        # Extraire le nombre de spectateurs
        viewers.append(card.find_element(By.XPATH, f"//p//a[contains(@data-a-target, 'card-{i}')]").text)

        # Extraire le lien vers la catégorie du jeu
        tag_elements = card.find_elements(By.XPATH, ".//button[@aria-label]//span")
        tags.append([tag.text for tag in tag_elements])

    except Exception as e:
        print(f'Erreur de récupération à la position {i}.')

# On range toutes les informations dans une dataframe

data_twitch= pd.DataFrame(list(zip(game_title, viewers, tags)), columns=["Game", "Viewers", "Tags"]) #Dataframe final

presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located
wait = WebDriverWait(driver, 5)
data_youtube=pd.DataFrame()

# Cette boucle permet de parcourir tous les jeux contenus dans notre dataframe Twitch sur Youtube. Il faut changer le paramètre len(data_twitch) pour echercher moins de jeux

for k in range(0,len(data_twitch)):

    # A chaque itération, on initialise nos tableaux pour concaténer nos informations dans la dataframe sans doublons

    game= []
    tags= []
    video_title= []
    link= []
    channel= []
    views= []
    date= []

    # Navigation vers le ième jeu de notre datafrme Twitch

    driver.get('https://www.youtube.com/results?search_query={}'.format(str(data_twitch["Game"][k])))
    
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

    recent_tab_position= 4
    recent_tab = wait.until(visible((By.XPATH, f"(//tp-yt-paper-tab[@role='tab'])[{recent_tab_position}]")))
    recent_tab.click()

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

    
    total_grid= driver.find_element(By.XPATH, "//div[contains(@id,'items') and contains(@class, 'style-scope ytd-grid-renderer')]")

    grids= total_grid.find_elements(By.XPATH, ".//ytd-grid-video-renderer")

    for grid in grids:

        video_title.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").text)
        link.append(grid.find_element(By.XPATH, ".//a[contains(@id, 'video-title')]").get_attribute("href"))
        channel.append(grid.find_element(By.XPATH, ".//ytd-channel-name").text)
        metadata= grid.find_elements(By.XPATH, ".//div[contains(@id, 'metadata-line')]")
        views.append(metadata[0].text)
        date.append(metadata[1].text)

    # On crée une dataframe temporaire contenant les informations de la vidéo en cours de scraping et on concatène toutes les dataframes temporaires pour obtenir la dataframe finale.

    game.append(data_twitch["Game"][k])
    tags.append(data_twitch["Tags"][k])

    temp_df= pd.DataFrame(list(zip(game, video_title, channel, views, date, tags, link)))
    data_youtube= pd.concat([data_youtube,temp_df], axis=0)

driver.quit()

# On renomme correctement les colonnes et on effectue un foramttage de la colonne "Nombre de vues"

data_youtube.to_csv('data.csv')

sys.exit()
data_youtube.columns = ['Game', 'Video title', 'Channel', 'Views', 'Date', 'Tags', 'Link']
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