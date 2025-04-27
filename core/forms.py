from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comentario

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'username': '',  # Dejar la ayuda de texto vacía para quitar el mensaje
        }

    password1 = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repetir contraseña')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Establece que no es un administrador ni superusuario
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }