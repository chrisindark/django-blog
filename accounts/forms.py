from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.conf import settings
from .models import User, UserFile


MIN_LENGTH = 8
ALPHABET = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets are allowed.')
ALPHANUMERIC = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphabets and numbers are allowed.')
MONTHS = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

YEARS = range(datetime.now().year, 1972 - 1, -1)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email', 'password1', 'password2',
        )

    def clean_password1(self):
        # Check that the password entries match
        password1 = self.cleaned_data.get('password1')
        # At least MIN_LENGTH long
        if len(password1) < MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % MIN_LENGTH)

        # # At least one letter and one non-letter
        # first_isalpha = password1[0].isalpha()
        # if all(c.isalpha() == first_isalpha for c in password1):
        #     raise forms.ValidationError(
        #         "The new password must contain at least one letter and at least one digit or" \
        #         " punctuation character.")
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def authenticate(self):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        user = authenticate(email=email, password=password1)
        return user

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = (
            'email', 'password',
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
           raise forms.ValidationError({'email': "Email does not exist."})
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError({'password': "Password is incorrect."})
        return self.cleaned_data

    def authenticate(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class UserSetPasswordForm(forms.Form):
    """
    A form that lets a user set their password without entering the old
    password
    """
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(label="New password confirmation", widget=forms.PasswordInput, required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        # Check that the password entries match
        password1 = self.cleaned_data.get('new_password1')
        # At least MIN_LENGTH long
        if len(password1) < MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % MIN_LENGTH)

        # At least one letter and one non-letter
        # first_isalpha = password1[0].isalpha()
        # if all(c.isalpha() == first_isalpha for c in password1):
        #     raise forms.ValidationError(
        #         "The new password must contain at least one letter and at least one digit or" \
        #         " punctuation character.")
        return password1

    def clean_new_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password1')
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user
    """
    email = forms.CharField(disabled=True, max_length=255)
    username = forms.CharField(required=False, max_length=255, validators=[ALPHANUMERIC])
    first_name = forms.CharField(required=False, max_length=255, validators=[ALPHABET])
    last_name = forms.CharField(required=False, max_length=255, validators=[ALPHABET])
    date_of_birth = forms.DateField(required=False)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'date_of_birth',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 0 and len(username) < MIN_LENGTH:
            raise forms.ValidationError("The username must be at least %d characters long." % MIN_LENGTH)
        return username


class UserPasswordChangeForm(UserSetPasswordForm):
    """
    A form that lets a user change their password to a new password
    """
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput, required=True)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password


class FileForm(forms.ModelForm):
    file = forms.FileField(label='Select a file')

    class Meta:
        model = UserFile
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')

        #validate content type
        main, sub = file.content_type.split('/')
        if not (main == 'image' and sub in ('jpeg', 'pjpeg', 'gif', 'png',)):
            raise forms.ValidationError("Please use a JPEG, or PNG image.")
        return file
