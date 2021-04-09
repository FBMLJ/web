from django.urls import path

from produto import views

app_name="produto"
urlpatterns = [
    path('valor-total/', views.valor_total, name='valor-total'),
    path('<int:id>/apagar',views.delete, name='delete'),
    path('index', views.index, name="index"),
    path("new", views.form, name="new"),
    path("edit/<int:id>", views.edita, name="edita"),
    path("lista", views.lista, name="lista")

]