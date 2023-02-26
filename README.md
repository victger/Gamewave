# Trend_YT_Twitch
Dans le cadre de ce projet, nous avons été chargés de concevoir une application web en utilisant le package Flask. L'objectif est de récupérer des données sur le web, en utilisant des données scrapées.

Nous devons ensuite afficher ces données de manière optimale, en utilisant des fonctionnalités telles qu'un moteur de recherche ou des graphiques, par exemple. Pour y parvenir, nous utiliserons la bases de données Elasticsearch.

## Sujet du projet
Nous avons décidé d'exploiter les données présentes dans les cartes de jeux Youtube comme montré ci-contre :

![Image montrant les cartes de jeux sur Youtube](/images/youtube_card.jpg "Carte de jeu pour le jeu vidéo Apex Legends sur Youtube")

. En effet cet onglet permet de recenser les vidéos faites sur un jeu. Nous avons remarqué que cet onglet n'était pas bien optimisé et ne permettait pas de naviguer de façon optimale afin de trouver la vidéo qui correspond le mieux à nôtre besoin. 

Afin de selectionner les jeux pour lesquels nous allons récupérer les données des vidéos, nous avons voulu récupérer les 20 jeux les plus populaires du moment afin que notre projet fonctionne en temps réel et qu'il soit constamment à jour. Pour cela nous avons décider de récupérer sur le site de streaming "Twitch" le nom des 20 jeux avec le plus de spectateurs. 

**Sources :** 

 - Youtube : https://www.youtube.com/
 - Twitch : https://www.twitch.tv/

## User Guide

Voici les instructions à suivre afin de pouvoir faire fonctionner notre application.

**Installation**

 1. Vous devez avoir la dernière version de Python installée sur votre machine. l'installation peut se faire [ici](https://www.python.org/downloads/).
 2. Ensuite ouvrez votre terminal et clonez le projet :                             
 `git clone git@github.com:victger/Trend_YT_Twitch.git`
 3. Enfin, installez toutes les librairies que l'on va utiliser qui se trouvent dans le document "requirements.txt" : 
 ```
pip list --format=freeze > requirements.txt 
```
```
python -m pip install -r requirements.txt 
```

**Utilisation**
Pour lancer l’application sur Windows taper l’instruction suivante depuis le terminal :

```
python hello.py 
```
Vous pouvez maintenant accéder à l'application sur  votre navigateur à l’adresse suivante : [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Developper guide

 **Arbre du projet**
 ```  
Trend_YT_Twitch 

|-- static
    |--style.css
    
|-- templates  
    |--hello.html
    |--app.js
    
|-- hello.py 
|-- scrap_relation.ipynb 
|-- requirements.txt 
|-- README.md 
```
**Fonctions des fichiers**

  - **scrap_relation.ipynb** : 

Ce script Python utilise la bibliothèque Selenium pour automatiser la navigation sur le site Twitch, extraire des données de la page et les stocker dans un objet pandas DataFrame. 

 Le script commence par importer les bibliothèques nécessaires, notamment `selenium` pour la navigation Web, `pandas` pour la gestion de données, `time` pour ajouter une pause dans le script, et `ChromeDriverManager` pour installer et gérer le pilote Chrome.
 
Ensuite, le navigateur Chrome est initialisé avec `webdriver.Chrome()`. La méthode `get()` est utilisée pour naviguer vers la page Twitch Directory triée par le nombre de spectateurs.

Après une pause de 5 secondes pour permettre à la page de charger complètement, le script extrait les informations des cartes Twitch à l'aide de la méthode `find_elements()`. Les informations sont stockées dans une liste nommée "card".

Le script itère ensuite sur chaque carte en utilisant une boucle `for` et extrait les caractéristiques des cartes à l'aide de la méthode `split()` pour les séparer en une liste de chaînes de caractères. Ces caractéristiques sont stockées dans trois listes différentes: "jeu" contenant le nom du jeu, "nb_spec" contenant le nombre de spectateurs et "tags" contenant les tags associés à la chaîne Twitch.

Enfin, le script utilise la méthode `pd.DataFrame()` pour créer un objet pandas DataFrame à partir de ces listes. Les colonnes du DataFrame sont nommées "Jeu", "Nombre de spectateurs" et "Tags". Enfin, la méthode `quit()` est utilisée pour fermer le navigateur.

Le DataFrame final "data_twitch" contient donc toutes les informations extraites de la page Twitch Directory triée par le nombre de spectateurs.

Le deuxième script a pour objectif de récupérer les données de vidéos YouTube en rapport avec les jeux vidéo présents dans un dataframe "data_twitch". Pour cela, il utilise la bibliothèque Selenium pour automatiser l'interaction avec le navigateur web Google Chrome.
Plus précisément, pour chaque jeu dans "data_twitch", le script va naviguer sur la page YouTube de recherche en utilisant le nom du jeu comme terme de recherche. 

Ensuite, il va cliquer sur la première vidéo de la liste de résultats de recherche pour accéder à sa page.
Une fois sur la page de la vidéo, le script va extraire le nombre de spectateurs en temps réel en naviguant vers l'onglet approprié. Ensuite, il va extraire les informations des 100 premières vidéos suggérées dans la section "Vidéos similaires" en récupérant les informations de chaque vidéo telles que le titre, la chaîne, le nombre de vues, la date de publication et le jeu associé. Ces informations sont stockées dans un dataframe "data_youtube".
 - **hello.py** :
 - **hello.html** :
 - **style.css** :
 - **app.js** : 
