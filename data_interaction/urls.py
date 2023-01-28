from django.urls import path, include
from rest_framework import routers

from  .views import (
    UserViewSet, 
    GroupViewSet, 
    CategorieActeur, 
    AverageMarketProductsManufacturer, 
    Top10Markets,
    AverageMarketProductsManufacturerInTop10Markets,
    NbrProviderByMonth,
    Synchronizer,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
#router.register(r'categorie_acteur/<int:idcat>', CategorieActeur)



urlpatterns = [
    
    path('', include(router.urls)),
    
    #Question 1.1 (nombre de concurrents). Pour la catégorie d’identifiant 5, combien y a t il d’acteurs sur le marché ayant un produit de cette catégorie?
    path('categorie_acteur/<int:idcat>', CategorieActeur.as_view()),
    path('categorie_acteur/', CategorieActeur.as_view()),
    
    #Question 1.2. Pour la catégorie d’identifiant 5, quel est en moyenne le nombre de produits qu’un fabricant offre sur le marché?
    path('average/market_products_manufacturer/<int:idcat>',AverageMarketProductsManufacturer.as_view()),
    path('average/market_products_manufacturer/<int:idcat>/<int:idfab>',AverageMarketProductsManufacturer.as_view()),
    path('average/market_products_manufacturer/',AverageMarketProductsManufacturer.as_view()),
    
    #Question 2.2. Idem pour la question 1.2., avec des valeurs prises pendant les soldes d’hiver.
    path('average/market_products_manufacturer_sold/<str:months>',AverageMarketProductsManufacturer.as_view()),
    path('average/market_products_manufacturer_sold/<int:idcat>/<str:months>',AverageMarketProductsManufacturer.as_view()),
    path('average/market_products_manufacturer_sold/<int:idcat>/<int:idfab>/<str:months>',AverageMarketProductsManufacturer.as_view()),
    
    #Question 1.3. Quels sont le top 10 des magasins parmi les magID enregistrés dans la base? N.B.: il faut définir formellement la notion d’être dans le top 10
    path('top10market/',Top10Markets.as_view()),
    ##Question 2.3. Idem pour la question 1.3., avec des valeurs prises pendant les soldes d’hiver et celles d’été
    path('top10market/<str:months>',Top10Markets.as_view()),

    path('top10markets_by_seasson',Top10Markets.as_view()),

    #Question 1.4 (score de santé). Pour le fabricant d’identifiant 1664, et parmi le top 10 des magasins vendant les produits de la catégorie d’identifiant 5, quel est en moyenne la part du nombre de produits qu’offre le fabricant 1664 dans l’ensemble des produits de catégorie 5 en vente dans ces magasins?
    path('average/market_products_manufacturer_in_top10Markets/',AverageMarketProductsManufacturerInTop10Markets.as_view()),#no resolved problem
    path('average/market_products_manufacturer_in_top10Markets/<int:idcat>/<int:idfab>/',AverageMarketProductsManufacturerInTop10Markets.as_view()),#no resolved problem

    #Question 2.1 Pour la catégorie d’identifiant 5, combien y a t il d’acteurs sur le marché ayant un produit de cette catégorie en Janvier, en Février, et en Mars?
    path('nbrproviderbymonth/',NbrProviderByMonth.as_view()),
    path('nbrproviderbymonth/<int:idcat>',NbrProviderByMonth.as_view()),
    
    
    
    

    
    path('sync/',Synchronizer.as_view()),
]