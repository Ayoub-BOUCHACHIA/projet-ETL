from django.contrib.auth.models import User, Group
from django.db.models import Count
from .models import dataProducts, accordsVente
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, CategorieActeurSerializer

from rest_framework.views import APIView
from rest_framework.response import Response



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategorieActeur(APIView):
    def get(self, request, format=None, *args, **kwargs):
        idcat = kwargs.get('idcat', -1)

        #idcat = self.request.query_params.get("idcat", -1)
        print("idcat : ",idcat)
        providers = accordsVente.objects.filter(id_category=idcat).values_list('id_provider', flat=True).distinct()
        queryset = { 
            "cagory_id" : idcat,
            "count" : providers.count(),
            'id_provider' : list(providers)
            }

        #usernames = [user.username for user in User.objects.all()]
        return Response(queryset)

class AverageMarketProductsManufacturer(APIView):
    def get(self, request, format=None, *args, **kwargs):
        idcat = kwargs.get('idcat', -1)
        idfab = kwargs.get('idfab', -1)
        queryset = {}
        if idcat>=0 and idfab>=0:
            nb_products_with_provider_category = accordsVente.objects.filter(id_category=idcat,id_provider=idfab).values_list('id_product', flat=True).count()
            nb_markets_with_category = accordsVente.objects.filter(id_category=idcat).values_list('id_vente', flat=True).distinct().count()
            queryset.update({
                "cagory_id" : idcat,
                "provider_id" : idfab,
                "nb_markets_with_provider_categoru" : nb_products_with_provider_category,
                "nb_markets_with_category" : nb_markets_with_category,
                "mean": nb_products_with_provider_category/nb_markets_with_category

            })
        elif idcat>=0:
            list_of_fab_with_mean = []
            for idfab in list(accordsVente.objects.all().values_list('id_provider', flat=True).distinct()):
                nb_products_with_provider_category = accordsVente.objects.filter(id_category=idcat,id_provider=idfab).values_list('id_product', flat=True).count()
                nb_markets_with_category = accordsVente.objects.filter(id_category=idcat).values_list('id_vente', flat=True).distinct().count()
                if nb_products_with_provider_category:
                    list_of_fab_with_mean.append({
                        "cagory_id" : idcat,
                        "provider_id" : idfab,
                        "nb_markets_with_provider_categoru" : nb_products_with_provider_category,
                        "nb_markets_with_category" : nb_markets_with_category,
                        "mean": nb_products_with_provider_category/nb_markets_with_category

                    })
    
            queryset.update({
                'list_of_providers_with_mean' : list_of_fab_with_mean
            })
        return Response(queryset)


class Top10Markets(APIView):
    def get(self, request, format=None, *args, **kwargs):
        queryset = list((accordsVente.objects
            .values('id_vente')
            .annotate(count_providers=Count('id_provider', distinct=True), count_categorys=Count('id_category', distinct=True))
            .order_by("-count_providers","-count_categorys")
        ))[:9]

        return Response(queryset)

class AverageMarketProductsManufacturerInTop10Markets(APIView):
    #idfab = 526
    def get(self, request, format=None, *args, **kwargs):
        idfab = kwargs.get('idfab', -1)
        idcat = kwargs.get('idcat', -1)
        hello = accordsVente.objects.filter(id_category=5).values('id_provider').annotate(count=Count("*")).order_by("-count")
        queryset = list((accordsVente.objects.filter(id_provider=idfab,id_category=idcat)
            .values('id_vente')
            .annotate(count_providers=Count('id_provider', distinct=True), count_categorys=Count('id_category', distinct=True))
            .order_by("-count_providers","-count_categorys")
        ))[:9]

        return Response(hello)