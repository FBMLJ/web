from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from projeto import views, settings


urlpatterns = [
    path('', lambda request: redirect('carrinho/')),
    path('carrinho/', include('carrinho.urls')),
    path('produto/', include('produto.urls')),
    path('admin/', admin.site.urls),
    path('autenticacao/', include('autenticacao.urls')),
    path('fornecedores/', include('fornecedores.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

