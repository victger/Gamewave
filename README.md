# Trend_YT_Twitch
Dans le cadre de ce projet, nous avons été chargés de concevoir une application web en utilisant le package Flask. L'objectif est de récupérer des données sur le web, en utilisant des données scrapées.

Nous devons ensuite afficher ces données de manière optimale, en utilisant des fonctionnalités telles qu'un moteur de recherche ou des graphiques, par exemple. Pour y parvenir, nous utiliserons la bases de données Elasticsearch.

## Sujet du projet
Nous avons décidé d'exploiter les données présentes dans les cartes de jeux Youtube comme montré ci-contre :

![Image montrant les cartes de jeux sur Youtube](https://zupimages.net/up/23/08/rph0.png "Carte de jeu pour le jeu vidéo Apex Legends sur Youtube")

En effet cet onglet permet de recenser les vidéos faites sur un jeu. Nous avons remarqué que cet onglet n'était pas bien optimisé et ne permettait pas de naviguer de façon optimale afin de trouver la vidéo qui correspond le mieux à nôtre besoin. On peut voir sur l'image suivante que l'on ne peut pas trier les vidéos par date de mise en ligne, ni nombre de vues :

![Onglet "Récentes" de Youtube pour le jeu Apex Legends](https://zupimages.net/up/23/08/14nl.png "Onglet Récentes de Youtube pour le jeu Apex Legends")

Afin de selectionner les jeux pour lesquels nous allons récupérer les données des vidéos, nous avons voulu récupérer les 20 jeux les plus populaires du moment afin que notre projet fonctionne en temps réel et qu'il soit constamment à jour. Pour cela nous avons décidé de récupérer sur le site de streaming "Twitch" le nom des 20 jeux avec le plus de spectateurs. 

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

Avant tout, il est nécessaire (si ce n'est pas le cas) d'installer Docker sur sa machine et le conteneur Elastic Search. Une fois Docker installé, on lance le conteneur Elastic Search. On vérifie également que le port utilisé est bien le 9200. Si ce n'est pas le cas, on modifiera notre code à la ligne 156. 

Pour lancer l’application sur Windows taper l’instruction suivante depuis le terminal en vous plaçant à la racine du dossier téléchargé :

```
python main.py 
```

Le scraping est alors lancé et vous pouvez observer en temps réel l'avancée dans le navigateur.
Une fois cela fini, vous pouvez maintenant accéder à l'application sur  votre navigateur à l’adresse suivante : [http://127.0.0.1:5000](http://127.0.0.1:5000)

Vous pouvez alors observer le résultat du scraping. Par défaut, toutes les vidéos et les informations qui lui sont associées sont affichées. Il est possible de :
- Trier les informations selon le jeu vidéo
- Chercher des mots parmi différents champs qui sont à cocher en cliquant ensuite sur "Chercher"
- Accéder aux vidéos en cliquant sur le lien en question

## Developper guide

 **Arbre du projet**
 ```  
Trend_YT_Twitch 

|-- static
    |--style.css
    
|-- templates  
    |--hello.html
    |--app.js
    
|-- main.py
|-- requirements.txt 
|-- README.md 
```
**Fonctions des fichiers**

  - **main.py** : 

Ce script Python utilise la bibliothèque Selenium pour automatiser la navigation sur le site Twitch, extraire des données de la page et les stocker dans un objet pandas DataFrame. 

Le script commence par importer les bibliothèques nécessaires, notamment `selenium` pour la navigation Web, `pandas` pour la gestion de données, `time` pour ajouter une pause dans le script, et `ChromeDriverManager` pour installer et gérer le pilote Chrome.
 
Ensuite, le navigateur Chrome est initialisé avec `webdriver.Chrome()`. La méthode `get()` est utilisée pour naviguer vers la page Twitch triée par le nombre de spectateurs.

Le script itère ensuite sur chaque carte en utilisant une boucle `for` et extrait les caractéristiques des cartes à l'aide de la méthode `split()` pour les séparer en une liste de chaînes de caractères. Ces caractéristiques sont stockées dans trois listes différentes: "jeu" contenant le nom du jeu, "nb_spec" contenant le nombre de spectateurs et "tags" contenant les tags associés au jeu Twitch.

Enfin, le script utilise la méthode `pd.DataFrame()` pour créer un objet pandas DataFrame à partir de ces listes. Les colonnes du DataFrame sont nommées "Jeu", "Nombre de spectateurs" et "Tags". Enfin, la méthode `quit()` est utilisée pour fermer le navigateur.

Le DataFrame final "data_twitch" contient donc toutes les informations extraites de la page Twitch triée par le nombre de spectateurs.

Le deuxième script a pour objectif de récupérer les données de vidéos YouTube en rapport avec les jeux vidéo présents dans un dataframe "data_twitch". Pour cela, on utilise la bibliothèque Selenium pour automatiser l'interaction avec le navigateur web Google Chrome.
Plus précisément, pour chaque jeu dans "data_twitch", le script va naviguer sur la page YouTube de recherche en utilisant le nom du jeu comme terme de recherche. 

Ensuite, on clique sur la carte de jeu du jeu vidéo concerné.
Une fois sur la page, on extrait les informations des 100 premières vidéos suggérées dans la section "Récentes" en récupérant les informations de chaque vidéo telles que le titre, la chaîne, le nombre de vues, la date de publication, les tags et le jeu associé. Ces informations sont stockées dans un dataframe "data_youtube". On fait cela pour tous les jeux vidéos présents dans la dataframe data_twitch.

Par la suite, on rentre cette dataframe dans la base de données Elastic Search. On crée alors des requêtes afin que l'utilisateur puisse interagir avec nos données. On crée également des nouvelles pages pour effectuer nos requêtes.

Nos requêtes fonctionnent par recherche de mots dans nos données selon plusieurs champs possibles et par recherche de jeu parmi les jeux scrapés. On notera que par défaut, toutes les données sont affichées.

 - **index.html** :

Ce fichier HTML contient toutes les instructions HTML nécessaires à l'affichage de nos données. Le code est tout à fait basique mais contient quelques scripts et lignes de code Jinja2 expliquées. Vous pourrez trouver plus d'explications dans l'éditeur de texte.

 - **style.css** :

Ce fichier CSS permet un rendu amélioré de l'interface d enotre page HTML.

 - **app.js** : 

Ce fichier Javascript est un template permettant une amélioration de l'affichage de nos données.

## Voies d'amélioration

On rappelle que l'objectif initial de ce projet est de proposer à l'utilisateur une expérience améliorée de l'onglet "Récentes" des jeux vidéos présents sur Youtube grâce à la présence de filtres affinant la recherche. Bien que nous avons pu récupérer toutes les informations concernant les jeux les plus populaires et réalisé quelques fonctionnalités sommaires de tri, nous ne sommes pas parvenus à offrir de nombreuses fonctionnalités. C'est pourquoi ce projet présente beaucoup d'intérêt à être amélioré. Les points suivants sont notamment à explorer :

- Un filtrage par date
- Un filtrage par nombre de vues
- Une navigation plus intuitive, améliorée
- Une interface plus jolie
- Une interface responsive
- Une analyse poussée des caractéristiques (mots fonctionnant le mieux par exemple)
- La prise en compte de plus jeux vidéos et vidéos Youtube
- Un site internet en temps réel disponible 24/24

## Auteurs

Zakary BELKACEM, Victor GERARD
