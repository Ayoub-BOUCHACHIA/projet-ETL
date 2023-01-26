from .serializers import ProduitLogSerializer
from .models import dataProducts, accordsVente
import requests
import time


def handle_logProduits(lastlogid):
    currentLogID = lastlogid+1
    while True:
        response = requests.get('http://51.255.166.155:1353/logProduits/'+str(currentLogID)+'/')
        jsondata = response.json()
        try:
            if not dataProducts.objects.filter(id=currentLogID,date=jsondata['dateID'],id_product=jsondata['prodID'],id_category=jsondata['catID'],id_provider=jsondata['fabID']).exists():
                dataProducts(date=jsondata['dateID'],id_product=jsondata['prodID'],id_category=jsondata['catID'],id_provider=jsondata['fabID'])
                print('['+time.ctime()+'] Successfully added log id="%s"' % jsondata['logID'])
            currentLogID+=1
        except KeyError:
            break
    print('['+time.ctime()+'] Data refresh terminated.')


def handle_logAccordsVente(lastlogid):
    currentLogID = lastlogid+1
    while True:
        response = requests.get('http://51.255.166.155:1353/logAccordsVente/'+str(currentLogID)+'/')
        jsondata = response.json()
        try:
            if not accordsVente.objects.filter(id=currentLogID,date=jsondata['dateID'],id_product=jsondata['prodID'],id_category=jsondata['catID'],id_provider=jsondata['fabID'],id_vente=jsondata['magID']).exists():
                accordsVente(date=jsondata['dateID'],id_product=jsondata['prodID'],id_category=jsondata['catID'],id_provider=jsondata['fabID'],id_vente=jsondata['magID'])
                print('['+time.ctime()+'] Successfully added log id="%s"' % jsondata['logID'])
            currentLogID+=1
        except KeyError:
            break
    print('['+time.ctime()+'] Data refresh terminated.')
