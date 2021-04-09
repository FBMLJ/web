from django import forms


class QuantidadeForm(forms.Form):

    produto_id = forms.CharField(widget=forms.HiddenInput())

    # <input type="hidden" name="produto_id" required="" id="id_produto_id" value="xxx">

    quantidade = forms.IntegerField(
        min_value=0,
        max_value=99,
        widget=forms.TextInput(attrs={'class': 'form-control btn-secondary quantidade border-0',
                                      'style': 'text-align: center; background-color: #6c757d; width: 70px;',
                                      'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57)',
                                      'readonly': 'readonly'}),
        required=True
    )

    # <input type="text" name="quantidade" class="form-control btn-secondary quantidade"
    #        style="text-align:center; background-color: #6c757d; width: 70px;"
    #        readonly="readonly" required="" id="id_quantidade">