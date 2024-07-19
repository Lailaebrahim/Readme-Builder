# Import necessary modules
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import is_valid_github_username

# Define the SignUpForm class
class SignUpForm(UserCreationForm):
    """
    A form for user sign up with additional fields for email and GitHub username.
    """

    # Define form fields
    email = forms.EmailField(label='Email', max_length=256)
    github_username = forms.CharField(label='GitHub Username', max_length=256)

    class Meta(UserCreationForm.Meta):
        # Include additional fields in the form
        fields = UserCreationForm.Meta.fields + ('email', 'github_username',)

    def clean_email(self):
        """
        Clean and validate the email field.

        Raises:
            forms.ValidationError: If the email is already taken.

        Returns:
            str: The cleaned email.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken.')
        return email

    def clean_github_username(self):
        """
        Clean and validate the GitHub username field.

        Raises:
            forms.ValidationError: If the GitHub username is associated with another account
                                   or if it is invalid.
        
        Returns:
            str: The cleaned GitHub username.
        """
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
