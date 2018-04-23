from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
import binascii
import os
import urllib
import requests
import json
from django.contrib.auth import authenticate, login
from .models import User
from .backends import OAuthBackend


def google_callback(request):
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me'

    print(request.GET)
    req = request.GET
    if 'code' not in req:
        form = dict(
            oauth_errors=req['error']
        )
        return render(request, "registration/login.html", {'form': form})

    payload = dict(
        client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        redirect_uri=settings.GOOGLE_OAUTH2_CALLBACK_URL,
        code=request.GET['code'],
        grant_type='authorization_code'
    )

    print(payload)

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    res = json.loads(r.text)
    if 'access_token' not in res:
        form = dict(
            oauth_errors=res['error']
        )
        return render(request, "registration/login.html", {'form': form})

    headers = {'Authorization': 'Bearer {0}'.format(res['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    res = json.loads(r.text)
    print(res['emails'][0]['value'])

    user = authenticate(email=res['emails'][0]['value'])
    print('request: ', request)
    login(request, user)

    return redirect('post_list')


def google_login(request):
    request_token_url = 'https://accounts.google.com/o/oauth2/auth'

    if request.method == 'GET':
        payload = {
            'redirect_uri': settings.GOOGLE_OAUTH2_CALLBACK_URL,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'scope': 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
                     ' https://www.googleapis.com/auth/userinfo.profile',
            'approval_prompt': 'force',
            'access_type': 'offline',
            'response_type': 'code',
        }

        request_token_url = request_token_url + '?' + urllib.parse.urlencode(payload)
        return redirect(request_token_url)


def github_callback(request):
    request = request.GET
    if 'code' in request:
        url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': settings.GITHUB_OAUTH2_CLIENT_ID,
            'client_secret': settings.GITHUB_OAUTH2_CLIENT_SECRET,
            'code': request.get('code')
        }
        headers = {'Accept': 'application/json'}
        r = requests.post(url, params=payload, headers=headers)
        response = r.json()
        # get access_token from response and store in session
        if 'access_token' in response:
            print(response['access_token'])
            # do something with the access token
        else:
            form = dict(
                oauth_errors=response['error']
            )
            return render(request, "registration/login.html", {'form': form})
        # send authenticated user where they're supposed to go
        return redirect('post_list')

    form = dict(
        oauth_errors=request['error']
    )
    return render(request, "registration/login.html", {'form': form})


def github_login(request):
    request_token_url = 'http://github.com/login/oauth/authorize'

    if request.method == 'GET':
        payload = {
            'redirect_uri': settings.GITHUB_OAUTH2_CALLBACK_URL,
            'client_id': settings.GITHUB_OAUTH2_CLIENT_ID,
            'scope': 'user public_repo',
            'state': binascii.hexlify(os.urandom(10)).decode(),
            'allow_signup': True
        }

        request_token_url_full = request_token_url + '?' + urllib.parse.urlencode(payload)
        return redirect(request_token_url_full)
