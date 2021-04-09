from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nome = models.CharField(max_length=70, db_index=True, unique=True)
    slug = models.SlugField(max_length=70)

    class Meta:
        db_table='categoria'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('carrinho:lista_produtos_por_categoria', args=[self.slug])