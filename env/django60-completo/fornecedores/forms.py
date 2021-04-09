from django.forms import ModelForm, CharField,TextInput
from .models import Fornecedores
from django.core.exceptions import ValidationError


class FornecedoresForm(ModelForm):
    cnpj = CharField(max_length=14, min_length=14, widget=TextInput(attrs={'type':'number'}))
    telefone = CharField( widget=TextInput(attrs={'type':'number'}))
    class Meta:
        model = Fornecedores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nome'].error_messages={'required': 'Campo obrigatório.'}
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['endereco'].error_messages={'required': 'Campo obrigatório'}
        self.fields['endereco'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['telefone'].error_messages={'required': 'Campo obrigatório'}
        self.fields['telefone'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['cnpj'].error_messages={'required': 'Campo obrigatório'}
        self.fields['cnpj'].widget.attrs.update({'class': 'form-control form-control-sm', 'unique': 'CNPJ duplicado.'})

    def clean_cnpj(self):
        data = self.cleaned_data["cnpj"]
        if len(data) != 14:
            raise ValidationError("CNPJ inválido")
        product = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        inteiros = data[:12]
        while len(inteiros)<14:
            r = sum([int(x)*y for (x,y) in zip(inteiros, product)]) % 11
            if r > 1:
                r = 11 - r
            else:
                r = 0
            inteiros += str(r)
            product.insert(0,6)
        if inteiros != data:
            raise ValidationError("CNPJ inválido")
        return data
    


