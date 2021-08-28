#-*- coding: utf-8 -*-
from django import forms
from Soluciones.models import soluciones
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Formulario(forms.ModelForm):
    class Meta:
        model = soluciones
        fields ='__all__'


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Entrar nombre de Usuario', min_length=4, max_length=150)
    email = forms.EmailField(label='Entrar su correo electrónico')
    password1 = forms.CharField(label='Entrar su Clave', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme su Clave', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("El usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("El correo ya existe")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('Clave 1')
        password2 = self.cleaned_data.get('Clave 2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las claves no son iguales")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
