from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from projeto import settings


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.caminho_protegido = '/produto/'
        self.login_path = getattr(settings, 'LOGIN_URL')
        self.fecha_compra = getattr(settings, 'FECHA_COMPRA')

    def __call__(self, request):

        if (request.path == self.fecha_compra or request.path.startswith(self.caminho_protegido)) and \
            request.user.is_anonymous:
            return HttpResponseRedirect('%s?next=%s' % (self.login_path, request.path))
        else:
            if request.path.startswith(self.caminho_protegido) and \
               not request.user.is_anonymous and \
               not request.user.is_staff:
                raise PermissionDenied('Você não possui permissão para acessar este path: ' + request.path)

        response = self.get_response(request)

        return response