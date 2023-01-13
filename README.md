# Projet-Nas

## Objectif du projet

## Organisation du git
Celon les différents objectif du projet, le github se découpe celon 2 dossiers principaux

- Team_network <br />
Il contient les projets GNS3 de l'implémentation modèle utilisée ainsi qu'un plan de cette dernière. On y trouve aussi un fichier texte récapitulant les commandes de configuration des routeurs à réaliser pour l'implémentation des différents protocoles.

- Team_script <br />
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
Avant de pouvoir lancer le script, ouvrez un projet GNS3. <br />
Dans **Edit > Preferences > Server**, faire attention à paramétrer le **Host binding** en **localhost** et le **port** au **3090 TCP**. <br />
Pour que la connexion se fasse il faut aussi faire attention à avoir cocher la case *"Allow console connections to any local IP address"*

![Capture](https://user-images.githubusercontent.com/84526681/212342093-97cf70af-2805-445f-b2a1-0465d3af0277.PNG)

#### Lancer le script
```
python ./script.py`
```

## Organisation des données (JSON)
Notre fichier "data.json" représente notre configuration sous un format spécifique.
Il présente la structure data qui contient tous les routeurs de notre réseau.
On spécifie pour chaque routeur les informations suivantes :
	
	** Name du routeur
	 ** Son role [ CE , PE , R ]
	 ** Sa position X,Y
	 ** Les interfaces de ce routeur: 
	      Pour chaque interface on specifie :
			    -> Name de l'interface 
			    -> L'adresse IPv4 
			    -> On precise aussi le neighbor de ce Routeur sur cette interface 
	
Et on ajoute des informations sur les configurations VRF, BGP, OSPF, MPLS 
Ça dépend du Rôle du routeur

=> Routeur : R 
   	
	** ospf :
            process(process-id)
            area 
            router-id
=> Routeur : PE
	
	** ospf :
            process(process-id)
            area 
            router-id
	 ** bgp :
            process(Num de AS)
            router-id
            
Et on ajoute dans les configs des interfaces des PE une presecion sur si on fait MPLS sur cette interface ou pas ==>> "config_ospf_mpls": false OR true

=> Routeur : CE
  	
	** bgp :
            AS 
            router-id
  	** vrf :
            Name de la vrf
            rd = route distinguisher 
            route = route target 


## Implémentation réalisée
Plan du modèle servi pour l'implémentation 2

-Le cœur du réseau est constitué des routeurs « provider » R1, R2, R3 et R4. On a sur les bordures, les routeurs PE1 et PE4 (provider edge). Et finalement les clients 
(customer edge) reliés à leurs PE : CE1, CE2, CE3 et CE4. 

-On a les protocoles MPLS et LDP sur les 6 routeurs : R1, R2, R3, R4, PE1 et PE4. Ce protocole permet de créer des labels et du coup setup plus rapidement les routeurs à chaque changement de topologie. Ces routeurs n’ont besoin que d’un seul label pour envoyer un packet vers un autre routeur. 
Un protocole OSPF dans le core (backbone) donc aussi sur les 6 routeurs (R1, R2, R3, R4, PE1 et PE4) ; l’objectif est d’établir la table de routage pour mettre en évidence l’état des liens et les tables d’adjacence donc tous les composants du coeur connaissent leurs voisins et vont choisir les labels pour ensuite les annoncer à ces voisins. 

-On implémente le protocole MP-BGP (extension au protocole BGP) sur les PE pour qu’ils puissent savoir quelles routes suivre pour envoyer les paquets dans le réseau de coeur : on utilise le protocole MP-BGP au lieu de BGP car ce dernier peut transporter plusieurs protocoles et d’étendre les capacités de BGP pour pouvoir transporter d’autres adresses telles que les adresses VPN niveau 3. Pour pouvoir connecter les sites du client A ou du client B entre eux, on va devoir créer une route vpn entre CE1/CE4 et CE2/CE3. Donc on aura un VRF par client pour qu’ils puissent s’envoyer des paquets sans partager leurs routes entre eux.

