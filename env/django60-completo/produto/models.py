from django.db import models
from django.urls import reverse

from categoria.models import Categoria

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=100, db_index=True, unique=True)
    descricao = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    # imagem = models.CharField(max_length=50, blank=True)
    imagem = models.ImageField(upload_to='images/')
    qtd_estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    data_cadastro = models.DateField()
    disponivel = models.BooleanField(default=False)

    class Meta:
        db_table='produto'

    def __str__(self):
        return self.nome

    def get_disponivel(self):
        return "Sim" if self.disponivel else "Não"

    def get_absolute_url(self):
        return reverse('carrinho:exibe_produto', args=[self.id, self.slug])






