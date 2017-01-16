from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    # avatar = models.CharField(max_length=255, default='/default/default.png')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User: {email}>'.format(email=self.email)


class File(models.Model):
    file = models.FileField(null=True, blank=True, upload_to='./images')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.file

    def __repr__(self):
        return '<File: {file}>'.format(file=self.file)


class UserFile(models.Model):
    user = models.ForeignKey('User')
    files = GenericRelation(File)


GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female'),
('P', 'Prefer not to answer'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.TextField(max_length=64, null=True, blank=True)
#    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    bio = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return '<UserProfile: {nickname}>'.format(nickname=self.nickname)
        return self.nickname
