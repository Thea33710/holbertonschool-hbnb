Description du projet HBNB

Ceci est le README du projet Holberton School HBNB – Partie 2. Cette partie fait suite à la partie 1, où nous avons défini les différents diagrammes de classes du projet global. Dans cette partie, nous allons implémenter  des API RESTful, en intégrant les modèles de classes et en établissant leurs liens avec le modèle Facade ainsi que les différentes API :

- Amenity : contient les differentes amenity disponible.

- User : contient les informations personnelles des utilisateurs (nom, prénom, email, mot de passe, etc.).

- Place : contient les logements disponibles sur la plateforme.

- Review : contient les avis des utilisateurs sur les logements.


Architecture des dossiers :

Dans l’optique de rendre notre plateforme HBNB plus claire, solide et compréhensible, nous avons décidé de créer une architecture structurée, répartie en plusieurs dossiers comme on peut le voir ci-dessous.

Arborescence du projet :

(Ajouter ici une capture d’écran ou un schéma de l’arborescence des dossiers)

Explication des dossiers :

- app/ : contient le code principal de l’application.
- api/ : héberge les points de terminaison de l’API, organisés par version (ex. v1/).
- models/ : contient les classes représentant la logique métier.
- services/ : contient l’implémentation du modèle Facade, gérant l’interaction entre les couches.
- persistence/ : contient le dépôt en mémoire. → Ce module sera ultérieurement remplacé par une solution basée sur une base de données SQLAlchemy.
- run.py : point d’entrée pour l’exécution de l’application Flask.
- config.py : contient les variables d’environnement et les paramètres de configuration.
- requirements.txt : liste les dépendances Python nécessaires au projet.
- README.md : contient toutes les informations utiles au fonctionnement de la plateforme.


Configuration de l’environnement :

Pour que notre serveur de test puisse fonctionner, il est nécessaire au préalable de télécharger certains prérequis.

Installation des prérequis :

pip install -r requirements.txt
(photo ?)

pip install flask

pip install flask-restx

python3 run.py

Lancement du serveur Flask :
(photo du serveur ?)

(photo des différentes commandes dans le terminal ?)


Exemples de cas d’utilisation :

Ci-dessous, nous pouvons voir les différents codes de réponse HTTP une fois le serveur en ligne lors de différentes manipulations, ainsi que certains codes de retour qui devront être implémentés à l’avenir lors de l’avancement du projet :

- 200 : Requête réussie.

- 401 : Utilisateur non authentifié.

- 403 : Accès refusé.

- 404 : Ressource non trouvée.

- 500 / 502 / 503 : Erreurs serveur.

- 504 : Délai d’attente dépassé.

(photo des différentes réponses pour chaque code)

Auteurs

- Thea Prolongeau 

- Dorian Oufer 
