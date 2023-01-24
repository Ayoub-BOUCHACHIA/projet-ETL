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
