from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password, backend='main.backends.UserBackend')
            print(user)
            if user is None:
                print('user is none')
            login(request, user)
            return redirect('home')

    signupform = SignUpForm()
    context = {
        'signupform': signupform
    }
    return render(request, 'main/login-page.html', context)


def get_home(request):
    return render(request, 'main/home.html')
