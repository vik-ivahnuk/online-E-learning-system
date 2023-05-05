from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from .models import User


# class SignUpForm(Form):
#     username = forms.CharField(
#         label='Username',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'line-input',
#             'placeholder': 'Username'
#         })
#     )
#     email = forms.EmailField(
#         label='Email',
#         max_length=50,
#         widget=forms.EmailInput(attrs={
#             'class': 'line-input',
#             'placeholder': 'Email'
#         })
#     )
#     first_name = forms.CharField(
#         label='First name',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'line-input',
#             'placeholder': 'First name'
#         })
#     )
#     last_name = forms.CharField(
#         label='Last name',
#         max_length=50,
#         widget=forms.TextInput(attrs={
#             'class': 'line-input',
#             'placeholder': 'Last name'
#         })
#     )
#     password = forms.CharField(
#         label='Password',
#         max_length=50,
#         widget=forms.PasswordInput(attrs={
#             'class': 'line-input',
#             'placeholder': 'Password'
#         })
#     )


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # зашифрувати пароль
        if commit:
            user.save()
