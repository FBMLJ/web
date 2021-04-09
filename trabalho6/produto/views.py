from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProdutoForm
from .models import Produto
import json

# Create your views here.

def valor_total(request):
    obj = Produto.objects.all()
    valorTotal = 0
    for i in obj:
        valorTotal += i.valor_final()
    context = {
        "valor_final": valorTotal
    }
    
    return render(request, "produto/valor.html", context)

def lista(request):
    obj = Produto.objects.all()
    
    
    context = {
        "produtos": obj
    }

    return render(request, 'produto/lista.html', context)

def index(request):
    return render(request, 'produto/index.html')


def delete(request,id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return JsonResponse({"message": "produto removido"})
    
def form(request):
    
    form = ProdutoForm()
    if request.method=="POST":
        print(request.POST)
        form =  ProdutoForm(request.POST)
        if form.is_valid():
            obj = form.save()
            print("Objeto criado com sucesso")
            
            return JsonResponse({"message": "sucesso"  })
        print("Objeto não criado") 
    context = {
        "form": form
    }
    return render(request, 'produto/new.html', context)

def edita(request, id):
    produto = Produto.objects.get(id=id)
    if request.method=="POST":
        print(request.body)
        print((request.body))
        data = json.loads(str(request.body))
        print(data)
       

    return JsonResponse({"message": "erro"})

