🌐 Part 4 – Simple Web Client

Développement Front-End en HTML5, CSS3 et JavaScript ES6

Ce volet du projet consiste à créer un client web interactif et moderne permettant d’interagir avec l’API back-end développée dans les parties précédentes. Vous devrez implémenter une interface conforme aux maquettes fournies, gérer l’authentification, afficher des données dynamiques et permettre aux utilisateurs d’ajouter des avis.

🎯 Objectifs

Concevoir une interface utilisateur responsive et agréable.

Mettre en place la logique front-end permettant de communiquer avec l’API.

Gérer les données de manière sécurisée (ex. token JWT en cookie).

Appliquer de bonnes pratiques modernes en développement web (ES6+, Fetch API, DOM manipulation, etc.).

📚 Compétences visées

Maîtrise de HTML5, CSS3 et JavaScript ES6.

Utilisation d’AJAX / Fetch API pour communiquer avec un serveur.

Gestion d’authentification (token JWT, cookies, sessions).

Création d’une application web dynamique sans rechargement complet de page.

🧩 Découpage des tâches
🔹 Task 1 – Design

Finaliser les fichiers HTML et CSS selon les spécifications du design fourni.

Créer les pages suivantes :

Login

List of Places

Place Details

Add Review

🔹 Task 2 – Login

Implémenter l’authentification via l’API back-end.

Stocker le token JWT dans un cookie pour gérer la session utilisateur.

Prévoir les redirections nécessaires en cas d’erreur ou d’utilisateur déjà connecté.

🔹 Task 3 – List of Places

Récupérer et afficher la liste complète des lieux depuis l’API.

Mettre en place un filtrage côté client (ex : par pays).

Rediriger systématiquement vers la page de login si l'utilisateur n'est pas authentifié.

🔹 Task 4 – Place Details

Afficher les détails complets d’un lieu (fetch par ID).

Afficher la liste des avis associés.

Afficher le bouton / lien Add Review uniquement si l’utilisateur est authentifié.

🔹 Task 5 – Add Review

Mettre en œuvre le formulaire permettant d’ajouter un avis.

Soumettre les données à l’API.

Restreindre l’accès :

→ Si utilisateur non authentifié : redirect vers index.

🚀 Technologies utilisées

HTML5 – structure des pages

CSS3 – styles et mise en page responsive

JavaScript (ES6+) – logique applicative, appels API

Fetch API – communication asynchrone avec le back-end

JWT + Cookies – gestion des sessions
