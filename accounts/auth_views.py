from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
import urllib
import requests
import json
from django.contrib.auth import authenticate, login
from .models import User
from .backends import OAuthBackend


def google_callback(request):
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me'

    print('\n\n\n\n')
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

    print('\n\n\n\n\n\n\n\n\n')
    print(payload)

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    res = json.loads(r.text)
    print('\n\n\n\n\n\n\n\n\n')
    if 'access_token' not in res:
        form = dict(
            oauth_errors=res['error']
        )
        return render(request, "registration/login.html", {'form': form})

    headers = {'Authorization': 'Bearer {0}'.format(res['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    res = json.loads(r.text)
    print('\n\n\n\n\n\n\n\n\n')
    print(res['emails'][0]['value'])

    user = authenticate(email=res['emails'][0]['value'])
    print('\n\n\n\n\n\n\n\n\n')
    print('request: ', request)
    login(request, user)

    return redirect('post_list')


def google_login(request):
    request_token_url = 'https://accounts.google.com/o/oauth2/auth'

    if request.method == 'GET':
        payload = {
            'redirect_uri': settings.GOOGLE_OAUTH2_CALLBACK_URL,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'scope': 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
            'approval_prompt': 'force',
            'access_type': 'offline',
            'response_type': 'code',
        }

        request_token_url_full = request_token_url + '?' + urllib.parse.urlencode(payload)
        return redirect(request_token_url_full)


# twitter = OAuth1Service(
#     name='twitter',
#     consumer_key='1yCuO4Sfvc3IGEIvE1rPdgfaK',
#     consumer_secret='RGjHoQB7fLcIVIUikbqMZfHqkFMff4N0wXeAUAHK1zamr2yYK8',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authorize',
#     base_url='https://api.twitter.com/1.1/')

# twitter_login = 0
# request_token = ''
# request_token_secret = ''


# class TwitterOauthView(views.APIView):
#     def post(self, request):
#         global login
#         global request_token, request_token_secret
#         context = RequestContext(request)
#         url = request.get_full_path()
#         # print url
#         parsed_url = urlparse(url)
#         # print parsed_url

#         if parsed_url.query == '':
#             context_dict = {'message': 'Welcome to social login'}
#             return render_to_response('index.html', context_dict, context)
#             login = 0

#         elif 'oauth_verifier' in parsed_url.query:
#             verifier = parse_qs(parsed_url.query)['oauth_verifier'][0]
#             session = twitter.get_auth_session(request_token,
#                                                request_token_secret,
#                                                method='POST',
#                                                data={'oauth_verifier': verifier})

