from django.forms import ModelForm
from .models import Produto
from django.core.exceptions import ValidationError


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['categoria','nome', 'quantidade', 'valor']