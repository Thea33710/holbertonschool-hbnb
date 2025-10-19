Description du projet HBNB

Ceci est le README du projet Holberton School HBNB – Partie 2. Cette partie fait suite à la partie 1, où nous avons défini les différents diagrammes de classes du projet global. Dans cette partie, nous allons implémenter  des API RESTful, en intégrant les modèles de classes et en établissant leurs liens avec le modèle Facade ainsi que les différentes API :

- Amenity : contient les differentes amenity disponible.

- User : contient les informations personnelles des utilisateurs (nom, prénom, email, mot de passe, etc.).

- Place : contient les logements disponibles sur la plateforme.

- Review : contient les avis des utilisateurs sur les logements.


Architecture des dossiers :

Dans l’optique de rendre notre plateforme HBNB plus claire, solide et compréhensible, nous avons décidé de créer une architecture structurée, répartie en plusieurs dossiers comme on peut le voir ci-dessous.

Arborescence du projet :

<img width="255" height="542" alt="organisation_hbnb" src="https://github.com/user-attachments/assets/62b20244-69e0-42f8-950a-f5013386b507" />


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

pip install flask

pip install flask-restx

python3 run.py

Lancement du serveur Flask :

<img width="2126" height="802" alt="serveur_flask" src="https://github.com/user-attachments/assets/099c2f9f-f742-4ce2-9ca0-11d71e2696eb" />


Exemples de cas d’utilisation :

Ci-dessous, nous pouvons voir les différents codes de réponse HTTP une fois le serveur en ligne lors de différentes manipulations, ainsi que certains codes de retour qui devront être implémentés à l’avenir lors de l’avancement du projet :

- 200 : Requête réussie.

- 401 : Utilisateur non authentifié.

- 403 : Accès refusé.

- 404 : Ressource non trouvée.

- 500 / 502 / 503 : Erreurs serveur.

- 504 : Délai d’attente dépassé.

Création d'un utilisateur
<img width="458" height="571" alt="new_user" src="https://github.com/user-attachments/assets/a368e852-43c0-4313-929d-59e24c04434f" />

Création d'un nouvel emplacemeent
<img width="441" height="673" alt="new_place" src="https://github.com/user-attachments/assets/ede0a6c4-dc4a-4bc2-bc88-994f0530d62f" />

Récupérer la liste de tous les équipements
<img width="439" height="518" alt="amenities" src="https://github.com/user-attachments/assets/e0f7fab2-889b-4cf9-a195-ff3dd055fd31" />

Création d'un avis
<img width="468" height="459" alt="new_review" src="https://github.com/user-attachments/assets/9df6eb90-d4a4-4172-961b-6195a355a01a" />

Suppression d'un avis
<img width="544" height="328" alt="delete" src="https://github.com/user-attachments/assets/9f1eb555-4b45-4040-91c8-a42dae5db76c" />


Auteurs :

- Thea Prolongeau 

- Dorian Oufer 
