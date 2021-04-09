from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AuthenticationFormCustomizado(AuthenticationForm):

    error_messages = {
        'invalid_login': 'Login inválido',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].error_messages={'required': 'Campo obrigatório'}
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-sm'})

        # <input type="text" name="username" autofocus="" autocapitalize="none" autocomplete="username"
        #        maxlength="150" required="" id="id_username">

        self.fields['password'].error_messages={'required': 'Campo obrigatório'}
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-sm'})

        # <input type="password" name="password" autocomplete="current-password" required=""
        #        id="id_password">


class UsuarioFormCustomizado(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = 'Nome'
        self.fields['first_name'].required = True

        self.fields['last_name'].label = 'Sobrenome'
        self.fields['last_name'].required = True

        self.fields['email'].label = 'Email'
        self.fields['email'].required = True
        self.fields['email'].error_messages = {'invalid': 'O campo Email é inválido.'}

        self.fields['username'].label = 'Usuário'
        self.fields['username'].error_messages = {
            'invalid': 'Usuário inválido. Use letras, números, @, ., +, -, _',
            'unique': 'Usuário já cadastrado.'
        }

        self.fields['password1'].label = 'Senha'
        self.fields['password1'].maxlength = 128

        self.fields['password2'].label = 'Confirmação de Senha'
        self.fields['password2'].maxlength = 128

        for field in self.fields.values():
            field.error_messages['required'] = \
                'Campo {nome_do_campo} de preenchimento obrigatório'.format(nome_do_campo=field.label)

        self.fields['password1'].validators.append(self.validate_password_strength)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    error_messages = {
        'password_mismatch': 'As senhas informadas não conferem.'
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        usuarios = User.objects.filter(email=email)

        if usuarios.exists():
            self.add_error('email', 'Email duplicado.')

        return email

    def validate_password_strength(self, valor):
        if len(valor) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')

        if not any(char.isdigit() for char in valor):
            raise ValidationError('A senha deve ter pelo menos 1 dígito.')

        if not any(char.isalpha() for char in valor):
            raise ValidationError('A senha deve ter pelo menos 1 letra.')





















