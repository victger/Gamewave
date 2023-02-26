# Trend_YT_Twitch
Ce projet est une application web Flask avec Elasticsearch, permettant de rechercher et de trier des données dans un index Elasticsearch. L'application prend en charge la recherche de texte libre, la recherche par champ et le tri par ordre croissant ou décroissant sur un champ spécifié.

## Sujet du projet
Nous avons décider d'utiliser des données des vidéos de l'onglet "catégorie" sur Youtube. En effet cet onglet permet de recenser les vidéos faites sur un jeu. Nous avons remarqué que cet onglet n'était pas bien optimisé et ne permettait pas de naviguer de façon optimale afin de trouver la vidéo qui correspond le mieux à nôtre besoin. 

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

 - scrap_relation.ipynb : 
 - hello.py :
 - hello.html :
 - style.css :
 - app.js : 
