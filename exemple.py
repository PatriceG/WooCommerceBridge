# coding: utf8
from woocommerce import API 

import pypyodbc
#import numpy as np
#import re
import json



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
    orders= wcapi.get("orders").json()

    print orders





#################

#data = '''[
#	{"index":"1","value":"non-member"},
#	{"index":"2","value":""},
#	{"index":"20","value":"aa"}
#]'''

 
# Si on veut un dico
#dictDim=json.loads(orders)
 
# Affichage dico
#for k in dictDim.viewkeys():
#	print "dim[%s]=%s" % (k, dictDim[k])
 
# Affichage dico (autre possibilité)
#for (k, v) in orders.viewitems():
#	print "dim[%s]=%s" % (k, v)
 
# Si on veut juste un tableau sur les valeurs (attention, les "value" seront stockées dans des indices itératifs allant de 0 à 2 et n'ayant plus rien avoir avec les nombres des index)
#tabDim=[x["value"] for x in json.loads(data)]
 
# Affichage liste
#for i in xrange(len(tabDim)):
#	print "i=%d, dim[%d]=%s" % (i, i, tabDim[i])
 
# Affichage liste (autre façon de faire)
#for (i, dim) in enumerate(tabDim)
#	print "i=%d, dim[%d]=%s" % (i, i, dim)

#######################################

	
  #  orders.encode('utf-8')

  #  print(orders)

    #affiche le nombre de commandes
   # orders_nb = len(orders)
   # print("%d commande(s)" % orders_nb)

  # tableau_data = np.array((2, 1), dtype='v')

   # billing = orders["billing"]
        #print billing
   
   # for key,value in billing.iteritems():
   #     print("%s => %s" % (key,value))
        
    #liste les commandes et certains attributs
   # for n in orders:
   #     liste.append(n["id"],n["order_key"])
   #     liste.append(n["id"],n["status"])        
        
    #    print("key = %s" % n["order_key"])
    #    print("id = %s" % n["id"])
    #    print("status = %s" % n["status"])
    #    print("date_created = %s" % n["date_created"])
    #    print("customer_note = %s" % n["customer_note"])
    #    print("first_name = %s" % n["billing"]["first_name"])
    #    print(" = %s" % n["billing"]["last_name"])
    #    print("address_1 = %s" % n["billing"]["address_1"])
    #    print("postcode = %s" % n["billing"]["postcode"])
    #    print("city = %s" % n["billing"]["city"])
    #    print("email = %s" % n["billing"]["email"])
    #    print("phone = %s" % n["billing"]["phone"])

        #print("payment_method = %s" % order["payment_method"])
        #print("date_paid = %s" % order["date_paid"])
        
        
   
#def getSafeValue(row,index):
#    if(index < len(row)):
#        return row[index]
#    else:
#        return ""



#def insertData(connection, row):
#    cur = connection.cursor()
#    cur.execute("INSERT INTO traite_bons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
#    (getSafeValue(row,0),getSafeValue(row,1),getSafeValue(row,2),getSafeValue(row,3),
#    getSafeValue(row,4),getSafeValue(row,5),getSafeValue(row,6),getSafeValue(row,7),
#    getSafeValue(row,8),getSafeValue(row,9),getSafeValue(row,10),getSafeValue(row,11),
#    getSafeValue(row,12),getSafeValue(row,13))).commit()
#    cur.close()    

#point d'entrée
if __name__ == '__main__':
    main()
