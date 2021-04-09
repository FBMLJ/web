from django.db import models

# Create your models here.
class Fornecedores(models.Model):
    nome = models.CharField( max_length=50, blank=False)
    endereco = models.CharField( max_length=50, blank=False)
    telefone = models.SlugField()
    cnpj = models.SlugField( max_length=50, blank=False, unique=True)