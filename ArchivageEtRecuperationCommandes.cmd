rem r�cup�ration et archivage des commandes
rem ce batch est appel� par une commande shell dans la proc�dure GestionCommandesInternet dans le moduleBoNS de SUITE
@echo off
cd c:\woocommercebridge

rem archivage car la commande python va effacer tous les enregistrements de la table 
copy woocommerce.mdb c:\woocommercebridge\ArchivesCommandes\woocommerce-%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%time:~3,2%%time:~6,2%.mdb

rem r�cup
woocommercebridge.py