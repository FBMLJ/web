from django import forms
from django.core.validators import RegexValidator

from categoria.models import Categoria
from produto.models import Produto
from projeto import settings


class PesquisaProdutoForm(forms.Form):

    nome = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'}),
        required=False)

    # <input type="text" name="nome" id="id_nome" class="form-control form-control-sm" maxlength="100">


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('nome', 'descricao', 'categoria', 'data_cadastro', 'preco', 'qtd_estoque', 'imagem', 'disponivel')
        localized_fields = ('preco',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nome'].error_messages={'required': 'Campo obrigatório.',
                                            'unique': 'Nome de produto duplicado.'}
        self.fields['nome'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['descricao'].error_messages={'required': 'Campo obrigatório'}
        self.fields['descricao'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['categoria'].error_messages={'required': 'Campo obrigatório'}
        self.fields['categoria'].queryset=Categoria.objects.all().order_by('nome')
        self.fields['categoria'].empty_label='--- Selecione uma categoria ---'
        self.fields['categoria'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['data_cadastro'].error_messages={'required': 'Campo obrigatório',
                                                     'invalid': 'Data inválida'}
        self.fields['data_cadastro'].input_formats=settings.DATE_INPUT_FORMATS
        self.fields['data_cadastro'].widget.attrs.update({'class': 'form-control form-control-sm'})

        self.fields['preco'].min_value=0
        self.fields['preco'].error_messages={'required': 'Campo obrigatório.',
                                             'invalid': 'Valor inválido.',
                                             'max_digits': 'Mais de 5 dígitos no total.',
                                             'max_decimal_places': 'Mais de 2 dígitos decimais.',
                                             'max_whole_digits': 'Mais de 3 dígitos inteiros.'}
        self.fields['preco'].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
        })

        self.fields['qtd_estoque'].min_value=0
        self.fields['qtd_estoque'].error_messages={
            'required': 'Campo obrigatório',
            'min_value': 'A quantidade deve ser maior ou igual a zero.'
        }
        self.fields['qtd_estoque'].widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
        })

        # self.fields['imagem'].error_messages={'required': 'Campo obrigatório'}
        # self.fields['imagem'].validators=[
        #     RegexValidator(regex='^[a-z]+\.(jpg|png|gif|bmp)$', message='Nome de imagem inválido.')]
        # self.fields['imagem'].widget.attrs.update({'class': 'form-control form-control-sm'})
        # self.fields['imagem'].required = True
        self.fields['imagem'].error_messages={'required': 'Campo obrigatório'}
        self.fields['imagem'].widget.attrs.update({'class': 'btn btn-outline-secondary btn-sm'})
        self.fields['imagem'].required = True

    # nome = forms.CharField(
    #     error_messages={'required': 'Campo obrigatório',
    #                     'unique': 'Nome de produto duplicado'},
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'})
    # )
    #
    # # <input type="text" name="nome" class="form-control form-control-sm" maxlength="100"
    # #        required="" id="id_nome">
    #
    # descricao = forms.CharField(
    #     error_messages={'required': 'Campo obrigatório'},
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100'})
    # )
    #
    # # <input type="text" name="descricao" class="form-control form-control-sm" maxlength="100"
    # #        required="" id="id_descricao">
    #
    # categoria = forms.ModelChoiceField(
    #     error_messages={'required': 'Campo obrigatório'},
    #     queryset=Categoria.objects.all().order_by('nome'),
    #     empty_label="--- Selecione uma categoria ---",
    #     widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    # )
    #
    # # <select name="categoria" class="form-control form-control-sm" required="" id="id_categoria">
    # #     <option value="" selected>--- Selecione uma categoria ---</option>
    # #     <option value="1">Frutas</option>
    # #     <option value="2">Legumes</option>
    # #     <option value="3">Verduras</option>
    # # </select>
    #
    # data_cadastro = forms.DateField(
    #     error_messages={'required': 'Campo obrigatório.',
    #                     'invalid': 'Data inválida.'},
    #     input_formats=settings.DATE_INPUT_FORMATS,
    #     widget=forms.DateInput(attrs={'class': 'form-control form-control-sm'})
    # )
    #
    # # <input type="text" name="data_cadastro" class="form-control form-control-sm" required=""
    # #        id="id_data_cadastro">
    #
    # preco = forms.DecimalField(
    #     localize=True,
    #     min_value=0,
    #     error_messages={'required': 'Campo obrigatório.',
    #                     'invalid': 'Preço inválido.',
    #                     'min_value': 'O preço deve ser maior ou igual a zero.',
    #                     'max_digits': 'Mais de 5 dígitos no total.',
    #                     'max_decimal_places': 'Mais de 2 dígitos decimais.',
    #                     'max_whole_digits': 'Mais de 3 dígitos inteiros.'},
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control form-control-sm',
    #         'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'
    #     })
    # )
    #
    # Beware that not all browsers support entering localized numbers in number input types.
    # Django itself avoids using them for fields having their localize property set to True.
    # # <input type="text" name="preco" class="form-control form-control-sm"
    # #        onkeypress="return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44"
    # #        required="" id="id_preco">
    #
    # qtd_estoque = forms.IntegerField(
    #     min_value=0,
    #     error_messages={'required': 'Campo obrigatório.',
    #                     'min_value': 'A quantidade deve ser maior ou igual a zero.'},
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control form-control-sm',
    #         'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'
    #     })
    # )
    #
    # # <input type="text" name="qtd_estoque" class="form-control form-control-sm"
    # #        onkeypress="return event.charCode >= 48 && event.charCode <= 57"
    # #        required="" id="id_qtd_estoque">
    #
    # imagem= forms.CharField(
    #     error_messages={'required': 'Campo obrigatório.'},
    #     validators=[RegexValidator(regex='^[a-z]+\.(jpg|png|gif|bmp)$', message='Nome de imagem inválido.')],
    #     widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '50'})
    # )
    #
    # # <input type="text" name="imagem" class="form-control form-control-sm" maxlength="50"
    # #        required="" id="id_imagem">
    #
    # # disponivel = forms.BooleanField(
    # #     widget=forms.CheckboxInput(),
    # #     required=False
    # # )
