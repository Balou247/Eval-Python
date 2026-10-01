# Exercice 1

## Question 1

Pour créer une station, il faut utiliser POST /stations.
Le code HTTP à retourner est 201 Created.

## Question 2

Si la station n'existe pas, il faut retourner le code HTTP 404.
La réponse peut être une erreur JSON avec un champ detail.

## Question 3

401 signifie que l'utilisateur n'est pas authentifié, par exemple s'il n'a pas envoyé de token.

403 signifie que l'utilisateur est authentifié mais qu'il n'a pas le droit d'accéder à la ressource, par exemple un utilisateur normal qui essaye d'accéder à une page administrateur.

# Exercice 3

Après avoir arrêté puis relancé l'API, les stations sont toujours présentes dans la base SQLite.
