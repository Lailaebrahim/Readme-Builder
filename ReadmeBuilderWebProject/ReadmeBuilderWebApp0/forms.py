from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from .utils import is_valid_github_username


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=256)
    github_username = forms.CharField(label='GitHub Username', max_length=256)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'github_username',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken.')
        return email

    def clean_github_username(self):
        github_username = self.cleaned_data.get('github_username')
        if User.objects.filter(github_username=github_username).exists():
            raise forms.ValidationError(
                'GitHub Username is associated with another account.')
        status = is_valid_github_username(github_username)
        if status == False:
            raise forms.ValidationError('Invalid GitHub Username.')
        elif status == None:
            raise forms.ValidationError('Something went wrong. Please try again later.')
        return github_username
