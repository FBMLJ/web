from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from autenticacao.forms import UsuarioFormCustomizado
from projeto import settings


def registra_usuario(request):
    if request.method == 'POST':
        form = UsuarioFormCustomizado(request.POST)

        if form.is_valid():
            novo_usuario = form.save()
            request.session['usuario_id'] = novo_usuario.id

            senha = form['password1'].value() # request.POST.get('password1')
            subject = 'Criação de Conta no Hortifruti.'
            message = novo_usuario.first_name + ' ' + novo_usuario.last_name + \
                ", \n\nSeguem os dados da sua conta no Hortifruti: " + \
                "\nConta: " +novo_usuario.username + \
                "\nSenha: " + senha + \
                "\n\nAtenciosamente, " + \
                "\nO Seu Hortifruti."
            from_email = settings.EMAIL_HOST_USER
            to_list = [novo_usuario.email]

            send_mail(subject, message, from_email, to_list, True) # True - falhar silenciosamente
            return redirect('autenticacao:exibe_usuario')
    else:
        form = UsuarioFormCustomizado()

    return render(request, 'autenticacao/registra_usuario.html', {'form': form})

def exibe_usuario(request):
    usuario = get_object_or_404(User, pk=request.session['usuario_id'])
    return render(request, 'autenticacao/exibe_usuario.html', {'usuario': usuario})

def sair(request):
    carrinho = request.session.get(settings.CARRINHO_SESSION_ID)
    logout(request)
    request.session[settings.CARRINHO_SESSION_ID] = carrinho
    return redirect(settings.LOGOUT_REDIRECT_URL)