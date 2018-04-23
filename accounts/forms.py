from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, SetPasswordForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import User, FileUpload


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
        if 0 < len(username) < MIN_LENGTH:
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


ALLOWED_FILE_TYPES = ('image', 'audio', 'video',)
ALLOWED_IMAGE_TYPES = ('image/jpeg', 'image/gif', 'image/png',
    'image/bmp', 'image/webp',)
ALLOWED_AUDIO_TYPES = ('audio/mpeg', 'audio/mp4', 'audio/wav', 'audio/ogg',)
ALLOWED_VIDEO_TYPES = ('video/mp4', 'video/webm', 'video/ogg',)


class FileForm(forms.ModelForm):
    file = forms.FileField(label='Select a file')

    class Meta:
        model = FileUpload
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if len(file.name) > 75:
            raise forms.ValidationError('File name should be less than or equal to 75 characters.')

        file_type = self.get_filetype(file)
        if file_type == 'image' and file.content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError('Image format should be of {0}.'.format(', '.join(ALLOWED_IMAGE_TYPES)))
        elif file_type == 'audio' and file.content_type not in ALLOWED_AUDIO_TYPES:
            raise forms.ValidationError('Audio format should be of {0}.'.format(', '.join(ALLOWED_AUDIO_TYPES)))
        elif file_type == 'video' and file.content_type not in ALLOWED_VIDEO_TYPES:
            raise forms.ValidationError('Video format should be of {0}.'.format(', '.join(ALLOWED_VIDEO_TYPES)))

        return file

    @staticmethod
    def set_filename(file):
        filename_list = file.name.lower().replace(' ', '_').split('.')
        ext = filename_list.pop()
        filename = ''.join(filename_list) + get_random_string(25) + '.' + ext
        return filename

    @staticmethod
    def get_filetype(file):
        if file.content_type.split('/')[0] not in ALLOWED_FILE_TYPES:
            raise forms.ValidationError({'file': 'File type should be of {0}'.format(', '.join(ALLOWED_FILE_TYPES))})
        return ALLOWED_FILE_TYPES[ALLOWED_FILE_TYPES.index(file.content_type.split('/')[0])]

    def save(self, commit=True):
        print(self)
        file = self.cleaned_data.get('file')
        self.file['file_content_type'] = file.content_type
        self.file['size'] = file.size
        self.file['name'] = self.set_filename(file)
