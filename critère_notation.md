Projet APP5 – Développement d’un (ou plusieurs) microservice(s)

Objectif

Le but de ce projet est de coder une API sous forme de microservice, en équipe de 3 à 4 personnes.
Dans l’idéal, les microservices des différents groupes devraient être capables de communiquer entre eux, mais ce n’est pas une obligation.

Le temps de développement est limité à 24 heures, donc il n’est pas attendu une API particulièrement complexe. L’important est de proposer une solution fonctionnelle et bien structurée, en tenant compte des niveaux variés des participants.

Contraintes techniques et fonctionnalités attendues
✅ Gestion d’au moins deux types d’objets
✅ Implémentation des requêtes API classiques : GET, POST, PUT, DELETE
✅ Pagination des résultats
✅ Filtrage des données via des paramètres optionnels (ex. : name, regex, etc.)
✅ Navigation dans l’arborescence des données (ex. : accéder aux documents d’un utilisateur via une URL comme http://localhost/user/1/document)
✅ Documentation OpenAPI 3 détaillant le fonctionnement de l’API
✅ Validation des entrées et sorties avec un validateur de données (ex. : Joi en Node.js)
✅ Conteneurisation avec Docker : L’application devra pouvoir être exécutée en local via docker-compose.
✅ Petit Rapport : Les difficultés rencontrées, les parties effectuées par chacun, les + ou - du cours (anonymes). (Pas de nombre de page minimum / maximum) 

✅ Les tests : unitaire, manuel avec Postman ou bien automatisé 

Options Bonus
⭐ Développement d’un front-end pour accompagner l’API (facultatif).
⭐ CI / CD : github action ou gitlab CI
⭐ Clean Architecture : Le beau code, toujours un +
⭐ Déploiement sous Kubernetes + monitoring, qui seront abordés en cours la semaine suivante.
⭐ Présentation finale du projet lors du dernier cours (notée ou non selon le choix des participants).

📌 Thèmes libres : jeux vidéo, site d’animés, gestion de playlists… Chaque équipe est libre de choisir son sujet tant qu’il respecte les contraintes techniques.