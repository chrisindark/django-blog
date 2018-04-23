from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email=email,
            password=password,
            **kwargs
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User: {email}>'.format(email=self.email)


def file_directory_path(instance, filename):
    return settings.FILE_UPLOAD_PATH + '{0}/{1}'.format(instance.user_id, instance.name)


class FileUpload(models.Model):
    user = models.ForeignKey('User')
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=file_directory_path, max_length=255)
    file_type = models.CharField(max_length=5)
    file_content_type = models.CharField(max_length=20)
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<File: {name}>'.format(name=self.name)


GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female'),
('P', 'Prefer not to answer'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.TextField(max_length=64, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    bio = models.TextField(max_length=1024, null=True, blank=True)
    # avatar = models.CharField(max_length=255, default='/default/default.png')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return '<UserProfile: {nickname}>'.format(nickname=self.nickname)
