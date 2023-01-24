from django.db import models

# Create your models here.


class dataProducts(models.Model):
    id_product = models.IntegerField()
    id_category = models.IntegerField()
    id_provider = models.IntegerField()
    date = models.DateField()


class accordsVente(models.Model):
    date = models.DateField()
    id_product = models.IntegerField()
    id_category = models.IntegerField()
    id_provider = models.IntegerField()
    id_vente = models.IntegerField()
    