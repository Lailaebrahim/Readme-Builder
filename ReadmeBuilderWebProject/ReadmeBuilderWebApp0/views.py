from django.template import loader
from django.http import HttpResponse
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import SignUpForm


def home(request):
    template = loader.get_template('ReadmeBuilderWebApp0/home.html')
    return HttpResponse(template.render(context={}, request=request))


def account(request):
    template = loader.get_template('ReadmeBuilderWebApp0/user_account.html')
    return HttpResponse(template.render(context={}, request=request))


def signin(request):
    template = loader.get_template('ReadmeBuilderWebApp0/signin.html')
    return HttpResponse(template.render(context={}, request=request))


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data.get('username'),
                        email=form.cleaned_data.get('email'),
                        github_username=form.cleaned_data.get(
                            'github_username'),
                        password=make_password(form.cleaned_data.get('password1')))
            user.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, "ReadmeBuilderWebApp0/signup.html", {"form": form})
