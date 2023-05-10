from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required(login_url='/')
def get_home(request):
    print('----------------------------            ', request.user)
    return render(request, 'main/home.html', {'user': request.user})


def index(request):
    logout(request)

    if request.method == 'POST':
        if 'sign-up' in request.POST:
            signupform = SignUpForm(request.POST)
            signinform = SignInForm()
            num = 2
            if signupform.is_valid():
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password, backend='main.backends.UserBackend')
                print(user)
                login(request, user)
                if request.user.is_authenticated:
                    return redirect('home')
        else:
            signinform = SignInForm(request.POST)
            signupform = SignUpForm()
            num = 1
            if signinform.is_valid():
                username = signinform.cleaned_data.get('username')
                raw_password = signinform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is None:
                    signinform.add_error(None, 'Неправильне ім\'я користувача або пароль.')
                else:
                    return redirect('home')
    else:
        signupform = SignUpForm()
        signinform = SignInForm()
        num = 0
    context = {
        'signupform': signupform,
        'signinform': signinform,
        'mode': num
    }

    return render(request, 'main/login-page.html', context)
