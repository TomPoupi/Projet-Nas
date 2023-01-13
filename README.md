# Projet-Nas

## Objectif du projet

## Organisation du git
Celon les différents objectif du projet, le github se découpe celon 2 dossiers principaux

- Team_network
Il contient les projets GNS3 de l'implémentation modèle utilisée ansi qu'un plan de cette implémentation. Ainsi qu'un fichier texte récapitulant les commandes de configuration des routeurs à réaliser pour l'implémentation des différents protocoles.

- Team_script
Il contient les scripts en python réalisés pour effectuer les configurations faites dans le dossier network de manière automatique pour un projet GNS3. Où les différentes données servant à cette implémantation sont organisées et stockées dans un fichier JSON.

## Comment lancer le projet
### Lancer le script de l'autoconfiguration

Telecharger le dossier script

#### Prérequis:
Pour faire le lien entre le script python et GNS3, nous utilisons la librairie gns3fy:
```
pip install gns3fy
```
Pour cela, il faut avoir la version 1.9 de pydantic:
```
pip install pydantic=1.9
```

#### Paramètres dans GNS3:
Avant de pouvoir lancer le script, ouvrez un projet GNS3.
Dans **Edit > Preferences > Server**, faire attention à paramétrerle host binding en localhost et le port au 3090 TCP.
Pour que la connexion se fasse il faut aussi faire attention à avoir cocher la case *"Allow console connections to any local IP address"*

#### Lancer le script
```
node ./script.py`
```

## Organisation des données (JSON)

## Implémentation réalisée
Plan du modèle servi pour l'implémentation
