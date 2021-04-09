from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from produto.forms import PesquisaProdutoForm, ProdutoForm
from produto.models import Produto

# @login_required(login_url='/autenticacao/login')
# @staff_member_required(login_url='/autenticacao/login')
# @user_passes_test(lambda u: u.is_superuser)
# @user_passes_test(lambda u: u.is_staff)
def lista_produto(request):
    form = PesquisaProdutoForm(request.GET)
    if form.is_valid():
        nome = form.cleaned_data['nome']
        lista_de_produtos = Produto.objects\
                                   .filter(nome__icontains=nome)\
                                   .order_by('nome')
        paginator = Paginator(lista_de_produtos, 3)
        pagina = request.GET.get('pagina')
        page_obj = paginator.get_page(pagina)

        print(lista_de_produtos)
        print(page_obj)

        return render(request, 'produto/pesquisa_produto.html', { 'produtos': page_obj,
                                                                  'form': form,
                                                                  'nome': nome })
    else:
        raise ValueError('Ocorreu um erro inesperado ao tentar recuperar um produto.')


# @user_passes_test(lambda u: u.is_staff)
def cadastra_produto(request):

    if request.POST:
        produto_id = request.session.get('produto_id')
        print('produto_id na sessão = ' + str(produto_id))
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            produto_form = ProdutoForm(request.POST, request.FILES, instance=produto)
        else:
            produto_form = ProdutoForm(request.POST, request.FILES)

        if produto_form.is_valid():
            produto = produto_form.save(commit=False)
            produto.slug = slugify(produto.nome)
            produto.save()
            if produto_id:
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
                del request.session['produto_id']
            else:
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')

            return redirect('produto:exibe_produto', id=produto.id)
    else:
        # if 'produto_id' in request.session:
        #     del request.session['produto_id']
        try:
            del request.session['produto_id']
        except KeyError:
            pass
        produto_form = ProdutoForm()

    return render(request, 'produto/cadastra_produto.html', {'form': produto_form})


# @user_passes_test(lambda u: u.is_staff)
def exibe_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    request.session['produto_id_del'] = id
    return render(request, 'produto/exibe_produto.html', {'produto': produto})


# @user_passes_test(lambda u: u.is_staff)
def edita_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto_form = ProdutoForm(instance=produto)
    request.session['produto_id'] = id
    return render(request, 'produto/cadastra_produto.html', {'form': produto_form})


# @user_passes_test(lambda u: u.is_staff)
def remove_produto(request):
    produto_id = request.session.get('produto_id_del')
    produto = get_object_or_404(Produto, id=produto_id)
    produto.imagem.delete()
    produto.delete()
    del request.session['produto_id_del']
    messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
    return render(request, 'produto/exibe_produto.html', {'produto': produto})




