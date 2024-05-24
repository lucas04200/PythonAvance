# TP Docker B3 IA DATA | Seguret Emile & Dechavanne Lucas
## Table des matières
1. [Informations](#informations)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Utilisation](#utilisation)

# TP DOCKER
***
## Informations
***
- Notre application permet de calculer des distances entre deux coordonnées géopraphique
- Etape de notre projet :
1) Nous avons tout d'abord instancié l'application react vide dans notre docker.
2) Ensuite, la création de la base de données et de l'API qui communique avec.
3) Création de deux routes, une en [POST] pour que l'utilisateur rentre ses coordonnées et une en [GET] pour recevoir l'historique des coordonnées.
4) Et enfin, il fallait ajouter cela à une interface web grâce au react qui communique avec la base de données postgre. 
## Technologies
***
Voici une liste des technologies utilisées :
- Docker
- python:3.9-slim
- postgres
- node:18-alpine
## Installation
***
- Téléchargez le dossier
- dans la racine du projet il faut lancer la commande "docker compose up --build"
# Utilisation
***
Effectuez la commande dans votre terminal : 
curl -X POST -H "Content-Type: application/json" -d '{"start_lat": 48.8566, "start_lon": 2.3522, "end_lat": 48.858844, "end_lon": 2.294351}' http://localhost:5000/route
Vous pouvez modifier les longitudes et latitudes comme souhaité, vous aurez un chaine de caractère qui est un format pour recuperer une liste de coordonnées.

Pour récupérer l'historique des coordonnées effectuez la requete : 
http://localhost:5000/coordinates

## Attention
***
- interface web non fonctionnelle ! 
## Crédit
***
Lucas dechavanne - Seguret Emile 
 
