# coding: utf8
from woocommerce import API 
 
wcapi = API(
        url="https://www.aeroclub-avranches.org/wp2/",
        consumer_key="ck_28b1fc5f3bf9fdf794f1cebd4320e3f5457545af",
        consumer_secret="cs_17dfa50b1a1eb8ecfab3a74fc8416f220e9df34b",
        query_string_auth=True,
        wp_api=True,
        version="wc/v2"
    )

def main():
    #récupère les commandes
    orders = wcapi.get("orders").json()
    print(orders)

    #affiche le nombre de commandes
    orders_nb = len(orders)
    print("%d commande(s)" % orders_nb)

    #liste les commandes et certains attributs
    for order in orders:
        key = order["order_key"]
        print("key = %s" % key)


#point d'entrée
if __name__ == '__main__':
    main()
