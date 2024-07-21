from django.template import loader
from django.http import HttpResponse
from .models import ReadmeWritterUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, SignInForm


def home(request):
    return render(request, 'ReadmeBuilderWebApp0/home.html')


@login_required
def account(request):
    user = request.user
    readme_user = ReadmeWritterUser.objects.get(user=user)
    form = SignUpForm(instance=user, initial={'github_username': readme_user.github_username,
                                              'github_token': readme_user.github_token})
    if form.is_valid():
        user.username = form.cleaned_data.get('username')
        user.email = form.cleaned_data.get('email')
        readme_user.github_username = form.cleaned_data.get('github_username')
        readme_user.github_token = form.cleaned_data.get('github_token')
        user.save()
        messages.success('Your Account has been updated successfully!')
        
    elif request.method == 'POST' and form.is_valid() == False:
        messages.warning(request, 'Please correct the error below.')
        
    return render(request, 'ReadmeBuilderWebApp0/user_account.html', {'form': form, 'readme_user': readme_user})

def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'You have been signed in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = SignInForm()
    return render(request, 'ReadmeBuilderWebApp0/signin.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = User.objects.create_user(username=form.cleaned_data.get('username'),
                                            email=form.cleaned_data.get(
                                                'email'),
                                            password=form.cleaned_data.get(
                                                'password1'),
                                            )

            readme_user = ReadmeWritterUser.objects.get(user=user)
            readme_user.github_username = form.cleaned_data.get(
                'github_username')
            readme_user.save()

            messages.success(
                request, 'Your account has been created successfully!')
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, "ReadmeBuilderWebApp0/signup.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return render(request, 'ReadmeBuilderWebApp0/home.html')
