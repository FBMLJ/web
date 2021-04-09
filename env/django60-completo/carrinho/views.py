import locale
from decimal import Decimal

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.signing import Signer
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from carrinho.carrinho import Carrinho
from carrinho.forms import QuantidadeForm
from categoria.models import Categoria
from produto.models import Produto

signer = Signer()

def lista_produtos(request, slug_da_categoria=None):
    categoria = None
    categorias = Categoria.objects.all().order_by('nome')
    lista_de_produtos = Produto.objects.filter(disponivel=True).order_by('nome')
    if slug_da_categoria:
        categoria = get_object_or_404(Categoria, slug=slug_da_categoria)
        lista_de_produtos = lista_de_produtos.filter(categoria=categoria).order_by('nome')

    paginator = Paginator(lista_de_produtos, 12)
    pagina = request.GET.get('pagina')
    try:
        produtos = paginator.page(pagina)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        produtos = paginator.page(paginator.num_pages)

    carrinho = Carrinho(request)
    lista_de_forms = []
    for produto in produtos:
        qtd = carrinho.get_quantidade_total(produto.id)
        lista_de_forms.append(QuantidadeForm(initial={'quantidade': qtd, 'produto_id': signer.sign(produto.id)}))

    if request.is_ajax():
        return render(request, 'carrinho/pagina_de_produtos.html', {'listas': zip(produtos, lista_de_forms)})

    return render(request, 'carrinho/lista_produtos.html', {'categorias': categorias,
                                                            'listas': zip(produtos, lista_de_forms),
                                                            'categoria': categoria})

def exibe_produto(request, id, slug_do_produto):
    produto = get_object_or_404(Produto, id=id)
    carrinho = Carrinho(request)
    qtd = carrinho.get_quantidade_total(id)
    form = QuantidadeForm(initial={'quantidade': qtd,
                                   'produto_id': signer.sign(id)})

    return render(request, 'carrinho/exibe_produto.html', {
        'produto': produto,
        'form': form
    })

def atualiza_carrinho(request):
    form = QuantidadeForm(request.POST)
    if form.is_valid():
        produto_id = signer.unsign(form.cleaned_data['produto_id'])
        quantidade = form.cleaned_data['quantidade']

        carrinho = Carrinho(request)
        if (quantidade == 0):
            carrinho.remover(produto_id)
            preco_total = 0.0
        else:
            carrinho.atualiza(produto_id, quantidade)
            preco_total = carrinho.get_preco_total(produto_id)

        qtd = carrinho.get_quantidade_carrinho()
        preco_carrinho = carrinho.get_preco_carrinho()

        print('***** id do produto = ' + produto_id +
              '  quantidade = ' + str(quantidade) +
              '  preço total do produto = ' + str(preco_total))
        print('***** qtd no carrinho = ' + str(qtd) +
              '  valor do carrinho = ' + str(preco_carrinho))

        locale.setlocale(locale.LC_ALL, 'pt_BR')
        preco_carrinho = locale.currency(preco_carrinho, grouping=True)
        preco_total = Decimal(preco_total)
        preco_total = locale.currency(preco_total, grouping=True)

        return JsonResponse({'quantidade': qtd,
                             'preco_carrinho': preco_carrinho,
                             'preco_total': preco_total})
    else:
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')

def exibe_carrinho(request):
    carrinho = Carrinho(request)
    produtos_no_carrinho = carrinho.get_produtos()

    lista_de_forms = []
    for produto in produtos_no_carrinho:
        lista_de_forms.append(QuantidadeForm(
            initial = {'quantidade': produto['quantidade'],
                       'produto_id': signer.sign(produto['id'])}
        ))
    valor_do_carrinho = carrinho.get_preco_carrinho()

    return render (request, 'carrinho/produtos_no_carrinho.html', {
        'listas': zip(produtos_no_carrinho, lista_de_forms),
        'valor_do_carrinho': valor_do_carrinho
    })

def fecha_compra(request):
    return render(request, 'carrinho/fecha_compra.html')






















