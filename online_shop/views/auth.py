from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from online_shop.forms import LoginForm, RegisterModelForm


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'online_shop/auth/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # password = form.cleaned_data.get('password')
            # user.is_active = True
            # user.is_superuser = True
            # user.is_staff = True
            # user.set_password(password)
            user.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'online_shop/auth/register.html', context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('product_list')
