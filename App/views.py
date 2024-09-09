from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth import logout
from .form import SignUpForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


# Sign-up

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('login')  # Redirect to the home page after sign-up
    else:
        form = SignUpForm()
    return render(request, 'authendication/sign_up.html', {'form': form})

# login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'authendication/login.html', {'form': form})

# log out

def logout_view(request):
    logout(request)
    return redirect('login')


# index

def index(request):
    user = request.user  # Get the logged-in user
    context = {'user': user}
    return render(request, 'index.html', context)


# Show 

def show(request):
    return render(request, 'show.html')