from django.contrib.auth.models import User, Group
from .models import accordsVente, dataProducts
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CategorieActeurSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        
        model = accordsVente
        fields = ['date', 'id_product','id_category', 'id_provider', 'id_vente']


class ProduitLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dataProducts
        fields = ("date","id_product","id_category","id_provider")



class accordsVenteSerializer(serializers.Serializer):
    date = serializers.DateField()
    id_product = serializers.IntegerField()
    id_category = serializers.IntegerField()
    id_provider = serializers.IntegerField()
    id_vente = serializers.IntegerField()



class accordsVenteEncoder():
    
    def default(self, obj):
        if isinstance(obj, accordsVente):
            return {
                "date" : obj.date,
                "product_id" : obj.id_product,
                "category_id" : obj.id_category,
                "provider_id" : obj.id_provider,
                "vente_id" : obj.id_vente
            
            }
    def list_dict(self,l):
        temp = []
        for instance in l:
            temp.append(self.default(instance))
        return temp