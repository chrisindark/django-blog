from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (password_reset,
    password_reset_done, password_reset_confirm,
    password_reset_complete, password_change, password_change_done)
from .models import User, File
from .forms import (UserCreationForm, LoginForm,
    UserSetPasswordForm, UserChangeForm, UserPasswordChangeForm,
    FileForm)
import sys


# Create your views here.
def user_register(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if not form.is_valid():
            return render(request, "registration/register.html", {'form': form})
        form.save()
        user = form.authenticate()
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('post_list')
        else:
            return render(request, 'registration/register.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, "registration/register.html", {'form': form})


def user_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if not form.is_valid():
            return render(request, 'registration/login.html', {'form': form})

        user = form.authenticate()
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('post_list')
        else:
            return render(request, 'registration/login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('post_list')


def user_password_reset(request):
    return password_reset(request,
        template_name='registration/user_password_reset_form.html',
        email_template_name='registration/user_password_reset_email.html',
        post_reset_redirect='user_password_reset_done',)


def user_password_reset_done(request):
    return password_reset_done(request,
        template_name='registration/user_password_reset_done.html')


def user_password_reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64=uidb64, token=token,
        template_name='registration/user_password_reset_confirm.html',
        set_password_form=UserSetPasswordForm,
        post_reset_redirect='user_password_reset_complete')


def user_password_reset_complete(request):
    return password_reset_complete(request,
        template_name='registration/user_password_reset_complete.html')


@login_required
def user_password_change(request):
    print('\n\n\n')
    print(request.user.has_usable_password())
    print('\n\n\n')
    if not request.user.has_usable_password():
        password_change_form = UserSetPasswordForm
    else:
        password_change_form = UserPasswordChangeForm

    print('\n\n\n')
    print(password_change_form)
    return password_change(request,
        template_name='registration/user_password_change.html',
        post_change_redirect='user_password_change_done',
        password_change_form=password_change_form)


@login_required
def user_password_change_done(request):
    return password_change_done(request,
        template_name='registration/user_password_change_done.html')


@login_required
def user_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, 'registration/user_account.html', {'form': form})
        else:
            return render(request, 'registration/user_account.html', {'form': form})
    else:
        form = UserChangeForm(instance=user)
        return render(request, 'registration/user_account.html', {'form': form})
