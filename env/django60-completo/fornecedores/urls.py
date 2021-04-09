from django.urls import path

from fornecedores import views


app_name = 'fornecedores'

urlpatterns = [

    
    path('', views.list_fornecedores,name='lista'),
    path('<int:id>', views.show,name='show'),
    path('novo', views.novo,name='novo'),
    path('<int:id>/editar', views.edita,name='editar'),
    path('<int:id>/deletar', views.delete,name="delete")
]
