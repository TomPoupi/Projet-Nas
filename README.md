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

-Le cœur du réseau est constitué des routeurs « provider » R1, R2, R3 et R4. On a sur les bordures, les routeurs PE1 et PE4 (provider edge). Et finalement les clients 
(customer edge) reliés à leurs PE : CE1, CE2, CE3 et CE4. 

-On a les protocoles MPLS et LDP sur les 6 routeurs : R1, R2, R3, R4, PE1 et PE4. Ce protocole permet de créer des labels et du coup setup plus rapidement les routeurs à chaque changement de topologie. Ces routeurs n’ont besoin que d’un seul label pour envoyer un packet vers un autre routeur. 
Un protocole OSPF dans le core (backbone) donc aussi sur les 6 routeurs (R1, R2, R3, R4, PE1 et PE4) ; l’objectif est d’établir la table de routage pour mettre en évidence l’état des liens et les tables d’adjacence donc tous les composants du coeur connaissent leurs voisins et vont choisir les labels pour ensuite les annoncer à ces voisins. 

-On implémente le protocole MP-BGP (extension au protocole BGP) sur les PE pour qu’ils puissent savoir quelles routes suivre pour envoyer les paquets dans le réseau de coeur : on utilise le protocole MP-BGP au lieu de BGP car ce dernier peut transporter plusieurs protocoles et d’étendre les capacités de BGP pour pouvoir transporter d’autres adresses telles que les adresses VPN niveau 3. Pour pouvoir connecter les sites du client A ou du client B entre eux, on va devoir créer une route vpn entre CE1/CE4 et CE2/CE3. Donc on aura un VRF par client pour qu’ils puissent s’envoyer des paquets sans partager leurs routes entre eux.

