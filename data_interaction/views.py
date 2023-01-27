from django.contrib.auth.models import User, Group
from django.db.models import Count
from .models import dataProducts, accordsVente
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import (
    UserSerializer,
    GroupSerializer,
    CategorieActeurSerializer,
    accordsVenteSerializer,
    accordsVenteEncoder
)

from rest_framework.views import APIView
from rest_framework.response import Response
from .util import handle_logProduits,handle_logAccordsVente

class Synchronizer(APIView):
    def get(self, request, format=None, *args, **kwargs):

        handle_logProduits(dataProducts.objects.last().id)
        handle_logAccordsVente(accordsVente.objects.last().id)
        
        return Response({})

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
        if idcat<0:
            providers = accordsVente.objects.all().values('id_category').annotate(nombre_de_concurrent=Count("id_provider", distinct=True))
        else:
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
        dict_season= {
            "ete" : ["6","7","8"],
            "hiver" : ["1","2","3"]
        }

        idcat = kwargs.get('idcat', -1)
        idfab = kwargs.get('idfab', -1)
        months = kwargs.get('months', None)

        queryset = {}
        if idcat>0:
            if idfab>0:
                if months:
                    nb_products_with_provider_category = accordsVente.objects.filter(id_category=idcat,id_provider=idfab,date__month__in=dict_season[months]).values_list('id_product', flat=True).count()
                    nb_markets_with_category = accordsVente.objects.filter(id_category=idcat,date__month__in=dict_season[months]).values_list('id_vente', flat=True).distinct().count()
                    queryset.update({
                        "solde" : months
                    })  
                else:
                    nb_products_with_provider_category = accordsVente.objects.filter(id_category=idcat,id_provider=idfab).values_list('id_product', flat=True).count()
                    nb_markets_with_category = accordsVente.objects.filter(id_category=idcat).values_list('id_vente', flat=True).distinct().count()

                queryset.update({
                    "cagory_id" : idcat,
                    "provider_id" : idfab,
                    "nb_products_with_provider_category" : nb_products_with_provider_category,
                    "nb_markets_with_category" : nb_markets_with_category,
                    "mean": nb_products_with_provider_category/nb_markets_with_category

                })
            else:
                list_of_fab_with_mean = []
                queryset.update({
                    "cagory_id" : idcat,
                })
                if months:
                    list_nb_products_for_provider_category = accordsVente.objects.filter(id_category=idcat, date__month__in=dict_season[months]).values('id_provider').annotate(nombre_produit=Count('id_product') ).order_by('-nombre_produit')
                    nb_markets_with_category = accordsVente.objects.filter(id_category=idcat,date__month__in=dict_season[months]).values_list('id_vente', flat=True).distinct().count()
                    queryset.update({
                        "solde" : months
                    })  
                else:
                    list_nb_products_for_provider_category = accordsVente.objects.filter(id_category=idcat).values('id_provider').annotate(nombre_produit=Count('id_product') ).order_by('nombre_produit')
                    nb_markets_with_category = accordsVente.objects.filter(id_category=idcat).values_list('id_vente', flat=True).distinct().count()
                queryset.update({
                    "nb_markets_for_category" : nb_markets_with_category,
                })
                for pv in list_nb_products_for_provider_category:
                    print(pv)
                    list_of_fab_with_mean.append({
                        "provider_id" : pv['id_provider'],
                        "mean": pv["nombre_produit"]/nb_markets_with_category

                    })
            
                queryset.update({
                    'list_of_providers_with_mean' : list_of_fab_with_mean
                })
        else:
            list_of_fab_foreach_cat_with_mean = []
            if months:
                list_nb_products_for_provider_category = accordsVente.objects.filter(date__month__in=dict_season[months]).values('id_category','id_provider').annotate(nombre_produit=Count('id_product') ).order_by('-nombre_produit')
                nb_markets_with_category = accordsVente.objects.filter(date__month__in=dict_season[months]).values('id_category').annotate(nombre_magasin=Count('id_vente',distinct=True) )
                queryset.update({
                    "solde" : months
                })
            else:
                list_nb_products_for_provider_category = accordsVente.objects.all().values('id_category','id_provider').annotate(nombre_produit=Count('id_product') ).order_by('-nombre_produit')
                nb_markets_with_category = accordsVente.objects.all().values('id_category').annotate(nombre_magasin=Count('id_vente',distinct=True))
            dict_cat_mean={}
            for ct in nb_markets_with_category:
                dict_cat_mean[ct['id_category']] = ct['nombre_magasin']
            queryset.update({
                "list_markets_with_count_of_category" : nb_markets_with_category,
            })
            for pv in list_nb_products_for_provider_category:
                
                list_of_fab_foreach_cat_with_mean.append({
                    'category_id' : pv['id_category'],
                    "provider_id" : pv['id_provider'],
                    'nombre_produit' : pv["nombre_produit"],
                    "mean": pv["nombre_produit"]/dict_cat_mean[pv['id_category']]

                })
        
            queryset.update({
                'list_of_fab_foreach_cat_with_mean' : list_of_fab_foreach_cat_with_mean
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
    rializer_class = CategorieActeurSerializer
    def get(self, request, format=None, *args, **kwargs):
        idfab = kwargs.get('idfab', -1)
        idcat = kwargs.get('idcat', 5)

        top_10_markets_for_category = list((accordsVente.objects
            .filter(id_category=5)
            .values('id_vente')
            .annotate(count_providers=Count('id_provider', distinct=True), count_categorys=Count('id_category', distinct=True))
            .order_by("-count_providers","-count_categorys").values_list('id_vente', flat=True).distinct())
        )[:9]
        list_of_product = accordsVente.objects.filter(id_vente__in=top_10_markets_for_category,id_provider=idfab)
        nb_products = list_of_product.values_list('id_product', flat=True).count()
        mean_per_market = nb_products/10
        print( list(list_of_product))
        from django.core.serializers import serialize
        import json
        return Response({
            "provider_id" : idfab,
            "category_id" : idcat,
            "top_10_market" : top_10_markets_for_category,
            "numbre_of_products" : nb_products,
            "mean_of_products" : mean_per_market,
            "list_of_product" :accordsVenteEncoder().list_dict(list_of_product)
        })


class NbrProviderByMonth(APIView):
    def get(self, request, format=None, *args, **kwargs):
        idcat = kwargs.get('idcat', 5)
        queryset = accordsVente.objects.filter(id_category=idcat,date__month__in=['1','2','3']).values('date__month').annotate(count_provider=Count("id_provider",distinct=True)).order_by("date__month")
        return Response(queryset)


class AverageMarketProductsManufacturerByMonth(APIView):
    def get(self, request, format=None, *args, **kwargs):
        idcat = kwargs.get('idcat', 5)
        idfab = kwargs.get('idfab', -1)
        month = kwargs.get('month',"ete")
        queryset = []
        if month == "hiver":
            months = ["6","7","8"]
        else:
            months = ["1","2","3"]
        print(idfab)
        if idfab>=0:
            products_with_provider_category = accordsVente.objects.filter(id_category=idcat,id_provider=idfab,date__month__in=months).values('date__month').annotate(count_product=Count("id_product",distinct=True)).order_by("date__month")
            
            i = 0
            for ppc in products_with_provider_category:
                nb_markets_with_category = accordsVente.objects.filter(id_category=idcat,date__month=ppc['date__month']).values_list('id_vente', flat=True).count()
                queryset.append({
                    "cagory_id" : idcat,
                    "provider_id" : idfab,
                    "month" : ppc['date__month'],
                    "markets_with_provider_categoru" : ppc,
                    "mean": ppc["count_product"]/nb_markets_with_category

                })
                i+=1

        else:
            list_of_fab_with_mean = []

            
            products_with_provider_category = accordsVente.objects.filter(id_category=idcat,date__month__in=months).values('id_provider','date__month').annotate(count_product=Count("id_product",distinct=True)).order_by("date__month")
            
            i = 0
            for ppc in products_with_provider_category:
                nb_markets_with_category = accordsVente.objects.filter(id_category=idcat,id_provider=ppc["id_provider"],date__month=ppc["date__month"]).values_list('id_vente', flat=True).count()
                list_of_fab_with_mean.append({
                    "cagory_id" : idcat,
                    "provider_id" : ppc["id_provider"],
                    "month" : ppc["date__month"],
                    "markets_with_provider_categoru" : ppc,
                    "nb_markets_with_category" : nb_markets_with_category,
                    "mean": ppc['count_product']/nb_markets_with_category

                })
                i+=1

            queryset.append({
                'list_of_mean_providers_by_month' : list_of_fab_with_mean
            })

        return Response(queryset)
