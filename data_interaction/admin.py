from django.contrib import admin

from .models import dataProducts, accordsVente

class dataProductsAdmin(admin.ModelAdmin):
    fields = ('date', 'id_product', 'id_category','id_provider')
    list_display = ('date', 'id_product', 'id_category','id_provider')
class accordsVenteAdmin(admin.ModelAdmin):
    fields = ('date','id_product', 'id_category','id_provider','id_vente')
    list_display = ('date','id_product', 'id_category','id_provider','id_vente')
    search_fields = ['id_provider']

admin.site.register(dataProducts,dataProductsAdmin)
admin.site.register(accordsVente,accordsVenteAdmin)