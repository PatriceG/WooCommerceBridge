# WooCommerceBridge
Interface entre GestAéro &amp; la boutique WooCommerce de l'Aéroclub des Grèves du Mont Saint-Michel

## Installation
Nécessite les librairies requests & pyodbc:
   
`pip install requests`

`pip install pyodbc`

La librairie woocommerce est embarquée car elle a été modifiée pour notre usage (désactivation de la pagination des résultats de recherche)

### Configuration
Ajouter les variables d'environnement suivantes à Windows:

`woo_consumer_key=consumer_key WooCommerce`

`woo_consumer_secret=consumer_secret WooCommerce`

L'application contrôle la présence de ces variables d'environnement au démarrage.

## Usage
L'application contrôle les erreurs, les affiche sur la console et trace dans le fichier de log **WooCommerceBridge.log**

### Récupération des commmandes
Lancement par:

`python WooCommerceBridge.py`

Récupération des commandes dans les états suivants: 

- pending
- processing
- on-hold

Le fichier woocommerce.mdb est créé s'il n'est pas présent. Les tables sont vidées si le ficher est déjà existant. Les différents attributs nécessaires sont récupérés.

### Modification d'une commande
Format de la ligne de commande: 
 
`python WooCommerceBridge.py [-h] [-m MODIFIE] [-e ETAT]`

Exemple, modification de l'état de la commande d'id 302:

`python WooCommerceBridge.py -m 302 -e "on-hold"`

La valeur de l'état est contrôlée par WooCommerce. Il renvoie une erreur en cas d'état non-valide.
