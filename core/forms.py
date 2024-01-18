from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label = '', widget = forms.TextInput(attrs = {"placeholder": "Логин"}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {"placeholder": "Пароль"}), label='')

    def clean_password(self):
        password = self.cleaned_data["password"]
        username = self.cleaned_data["username"]
        
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise ValidationError("Неверный email или пароль")
        else:
            if not(check_password(password, user.password)):
                raise ValidationError("Неверный email или пароль")
        return password
    

class ResetPassForm(PasswordResetForm):
    email = forms.EmailField(
        label = '',
        max_length = 254,
        widget = forms.EmailInput(attrs = {"autocomplete": "email", "placeholder": "email"}),
    )

class PassSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label = '',
        widget = forms.PasswordInput(attrs = {"autocomplete": "new-password", "placeholder": "новый пароль"}),
        strip = False
    )
    new_password2 = forms.CharField(
        label = '',
        strip = False,
        widget = forms.PasswordInput(attrs = {"autocomplete": "new-password", "placeholder": "подтверждение пароля"}),
    )


    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    "пароли не совпадают"
                )
        return password2