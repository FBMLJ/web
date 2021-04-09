from django.db import models
from categoria.models import Categoria

# Create your models here.
class Produto(models.Model):
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    quantidade =  models.IntegerField()
    valor = models.FloatField()
    def valor_final(self):
        return self.valor * self.quantidade