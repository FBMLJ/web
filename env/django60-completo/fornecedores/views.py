from django.shortcuts import render, redirect
from fornecedores.models import Fornecedores
from django.core.paginator import Paginator
from .forms import FornecedoresForm

# Create your views here.

def list_fornecedores(request):
    pag =1
    search = ""
    if 'page' in request.GET:
        pag = request.GET['page']

    if 'search' in request.GET:
        search  = request.GET["search"]
    fornecedores = Paginator(Fornecedores.objects.all().order_by('nome').filter(nome__contains=search),10).page(pag)
    
    context = {
        "fornecedores": fornecedores,
        "search": search
    }
    return render(request, 'fornecedores/index.html', context)

def novo(request):
    form  = FornecedoresForm()
    if request.method=="POST":
        
        form = FornecedoresForm(request.POST)
        if form.is_valid():
            obj = form.save()
            
            return redirect('/fornecedores/'+str(obj.id))
    context = {
        "form": form
    }
    return render(request, 'fornecedores/new.html', context)

def edita(request, id):
    fornecedor = Fornecedores.objects.get(id=id)
    form  = FornecedoresForm(instance = fornecedor)
    if request.method=="POST":
        
        form = FornecedoresForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
        return redirect('/fornecedores/'+str(id))
    context = {
        "form": form
    }
    return render(request, 'fornecedores/edit.html', context)


def delete(request, id):
    obj = Fornecedores.objects.get(id=id)
    obj.delete()
    return redirect('/fornecedores/')

def show(request, id):
    obj = Fornecedores.objects.get(id=id)
    context = {
        "fornecedor": obj
    }
    return render(request, 'fornecedores/show.html',context)