from django.urls import path, include
from rest_framework import routers

from  .views import (
    UserViewSet, 
    GroupViewSet, 
    CategorieActeur, 
    AverageMarketProductsManufacturer, 
    Top10Markets,
    AverageMarketProductsManufacturerInTop10Markets,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
#router.register(r'categorie_acteur/<int:idcat>', CategorieActeur)



urlpatterns = [
    path('', include(router.urls)),
    path('categorie_acteur/<int:idcat>', CategorieActeur.as_view()),
    path('average/market_products_manufacturer/<int:idcat>',AverageMarketProductsManufacturer.as_view()),
    path('average/market_products_manufacturer/<int:idcat>/<int:idfab>',AverageMarketProductsManufacturer.as_view()),
    path('top10markets/',Top10Markets.as_view()),
    path('AverageMarketProductsManufacturerInTop10Markets/<int:idcat>/<int:idfab>',AverageMarketProductsManufacturerInTop10Markets.as_view()),
]