from django.urls import path
from carrinho import views

app_name = 'carrinho'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('atualiza_carrinho/', views.atualiza_carrinho, name='atualiza_carrinho'),
    path('exibe_carrinho/', views.exibe_carrinho, name='exibe_carrinho'),
    path('fecha_compra/', views.fecha_compra, name='fecha_compra'),
    path('<slug:slug_da_categoria>/', views.lista_produtos, name='lista_produtos_por_categoria'),
    path('<int:id>/<slug:slug_do_produto>/', views.exibe_produto, name='exibe_produto')
]