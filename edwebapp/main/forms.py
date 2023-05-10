
from django.forms import ModelForm, Form, TextInput, EmailInput, PasswordInput, CharField
from .models import User
from django.core.exceptions import ValidationError


class SignInForm(Form):
    username = CharField(
        label='username',
        max_length=50,
        widget=TextInput(attrs={
            'class': 'line-input',
            'placeholder': 'Username'
        })
    )

    password = CharField(
        label='password',
        max_length=50,
        widget=PasswordInput(attrs={
            'class': 'line-input',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username:
            raise ValidationError("Поле username не може бути порожнім.")
        if not password:
            raise ValidationError("Поле password не може бути порожнім.")

        return cleaned_data


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        ]
        widgets = {
            'username': TextInput(attrs={
                'class': 'line-input',
                'placeholder': 'Username'
            }),
            'email': EmailInput(attrs={
                'class': 'line-input',
                'placeholder': 'Email'
            }),
            'first_name': TextInput(attrs={
                'class': 'line-input',
                'placeholder': 'First name'
            }),
            'last_name': TextInput(attrs={
                'class': 'line-input',
                'placeholder': 'Last name'
            }),
            'password': PasswordInput(attrs={
                'class': 'line-input',
                'placeholder': 'Password'
            })
        }

        error_messages = {
            'username': {
                'unique': "Цей username вже використовується"
            },
            'email': {
                'unique': "Цей email вже використовується"
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        users = User.objects.filter(username=username)
        if users.exists():
            raise ValidationError(self.fields['username'].error_messages['unique'], code='unique')
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            raise ValidationError(self.fields['email'].error_messages['unique'], code='unique')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
