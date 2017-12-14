# coding: utf-8
from __future__ import print_function
import os
import sys
import argparse
import logging
import pypyodbc
import requests
import time
from datetime import datetime
from woocommerce import API 

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def getEnv(key):
    """
    Retourne la valeur de la variable d'env spécifiée, ou une erreur si non-définie
    """
    try:  
        value = os.environ[key]        
        return value
    except KeyError: 
        msg = "Variable d'environnement '{}' non definie!".format(key)
        print(msg)
        logging.error(msg)
        sys.exit(1)


level = logging.INFO
logging.basicConfig(format='[%(asctime)-15s] %(levelname)s %(message)s', level=level, filename=getEnv("woo_bridge") + "WooCommerceBridge.log")

#init de l'API WooCommerce 
wcapi = API(
        url="https://www.aeroclub-avranches.org/wp2/",
        consumer_key=getEnv("woo_consumer_key"),
        consumer_secret=getEnv("woo_consumer_secret"),
        query_string_auth=True,
        wp_api=True,
        version="wc/v2"
    )

def createDatabase():
    """
    Crée la bdd, les tables et vide les tables si la bdd existe déjà
    """
    file = getEnv("woo_bridge") + "woocommerce.mdb"
    if(os.path.exists(file)):
        connection = pypyodbc.win_connect_mdb(file)
        #vide la bdd
        cur = connection.cursor()
        cur.execute("DELETE FROM woocommerce_produit").commit()
        cur.execute("DELETE FROM woocommerce_commande").commit()
        cur.close()
        return connection         
    else:
        pypyodbc.win_create_mdb(file)
        connection = pypyodbc.win_connect_mdb(file)
        #NumCommande est l'id de la commande
        fields = '''
        Id_Commande LONG,
        NumCommande LONG,
        StatutCommande VARCHAR(20),
        Date_creation DATETIME,  
        Prenom VARCHAR(25),
        Nom VARCHAR(25),
        Adresse VARCHAR(150),
        CodePostal VARCHAR(5),
        Ville VARCHAR(50),	
        Tel VARCHAR(20),
        Email VARCHAR(50),
        Type_Paiement VARCHAR(30),
        Date_Paiement DATETIME,
        Date_Termine DATETIME,
        Commentaire  VARCHAR(200)
        '''
        connection.cursor().execute('CREATE TABLE woocommerce_commande (%s);' % fields).commit()

        fields = '''
        Id_Produit INTEGER,
        Quantite BYTE,
        Id_Commande LONG
        '''
        connection.cursor().execute('CREATE TABLE woocommerce_produit (%s);' % fields).commit()
        return connection


def safeParseDate(d):
    """
    Parse une date sans planter si la chaine passée en param est nulle
    """
    global DATE_FORMAT    
    if d is not None:
        return datetime.strptime(d,DATE_FORMAT)
    else:
        return None

def insertData(connection, order):    
    """
    Insère la commande spécifiée & ses produits attachés, dans la bdd
    """
    cur = connection.cursor()
    #commande
    id_commande = order["id"]
    num_commande = order["number"]
    prenom = order["billing"]["first_name"]
    nom = order["billing"]["last_name"]
    statut_commande = order["status"]
    date_creation = safeParseDate(order["date_created"])
    adresse = order["billing"]["address_1"]
    code_postal = order["billing"]["postcode"]
    ville = order["billing"]["city"]
    tel = order["billing"]["phone"]
    email = order["billing"]["email"]
    type_paiement = order["payment_method_title"]
    date_paiement = safeParseDate(order["date_paid"])
    date_termine = safeParseDate(order["date_completed"])
    commentaire = order["customer_note"]
    

    logging.debug("insertData: %s",num_commande)
    cur.execute("INSERT INTO woocommerce_commande VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(id_commande,num_commande,statut_commande,date_creation,prenom,nom,adresse,code_postal,ville,tel,email,type_paiement,date_paiement,date_termine,commentaire)).commit()
   
    #produit(s)
    for line_item in order["line_items"]:
        logging.debug("produit: %s",line_item["name"])
        id_produit = line_item["product_id"]
        quantite = line_item["quantity"]
        cur.execute("INSERT INTO woocommerce_produit VALUES (?,?,?)",(id_produit,quantite,id_commande)).commit()
    
    cur.close()

def getOrdersByStatus(status):
    """
    Retourne les commandes qui sont dans l'état spécifié
    """
    global wcapi
    orders = wcapi.getEx("orders",{"per_page": 100, "status": status}).json()
    if not isinstance(orders,list):
            msg = orders["message"]
            print(msg)
            logging.error(orders)
            sys.exit(1)

    return orders

def getOrders():
    """
    Retourne les commande selon les critères choisis
    """    
    orders = getOrdersByStatus("pending")
    orders.extend(getOrdersByStatus("on-hold"))
    #orders.extend(getOrdersByStatus("any")) #TODO REMOVE!
    #affiche le nombre de commandes
    orders_nb = len(orders)
    logging.info("{} commande(s) trouvées".format(orders_nb))
    return orders
        

def updateOrder(order_id, order_status):
    """
    Met à jour la commande d'id spécifié, dans l'état spécifié
    """
    logging.info("mise à jour de la commande %s avec l'état %s",order_id,order_status)
    data = {"status": order_status}
    res = wcapi.put("orders/{}".format(order_id),data).json()
    logging.debug("res = %s",res)
    if "data" in res:
        msg = res["message"]
        print(msg)
        logging.error(res)
        sys.exit(1)
    


def main():           
    """
    Si aucun argument n'est passé: lit les commandes et les stocke dans la bdd woocommerce.mdb 
    Si -m id_commande -e etat_commande sont passés, modifie la commande spécifiée
    """
    parser = argparse.ArgumentParser(description='Interface avec WooCommerce')
    parser.add_argument("-m","--modifie",   help="Modifie la commande d'id spécifié", required=False)
    parser.add_argument("-e","--etat",   help="Etat de la commande à positionner", required=False)
    args = parser.parse_args()
    
    modif = args.modifie
    etat = args.etat

    if modif is not None:
        updateOrder(modif,etat)
    else:    
        connection = createDatabase()                    
        orders = getOrders()
        print(orders)
        for order in orders:
            insertData(connection, order)

        if(connection != None):
            connection.close()          
    
if __name__ == '__main__':
    main()
