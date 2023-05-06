from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def custom_login_required(view_func):
    decorated_view_func = login_required(view_func)

    def wrapper(request, *args, **kwargs):
        print(request.user)
        if not request.user.is_authenticated:
            return redirect('main')
        return decorated_view_func(request, *args, **kwargs)

    return wrapper


def index(request):

    if request.method == 'POST':
        if 'sign-up' in request.POST:
            print("\n\nSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS\n\n")
            signupform = SignUpForm(request.POST)
            signinform = SignInForm()
            num = 2
            print("FORM is :", signupform.is_valid())
            if signupform.is_valid():
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password, backend='main.backends.UserBackend')

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
                print(username, "---------", raw_password)
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



def get_home(request):
    return render(request, 'main/home.html', {'user': request.user})
