from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
import pandas as pd


def index(request):
    dogs = pd.read_csv('data/old_dogs.csv').to_dict('records')
    context = {
        'dogs': dogs,
    }
    return render(request, 'webapp/index.html', context)


def profile(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    return render(request, 'webapp/profile.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })


def update(request):
    return


def logout(request):
    django_logout(request)
    domain = 'dev-kvues7me.us.auth0.com'
    client_id = 'MKgBDuyKDlv2ljKatcWkJZfHULmVzYbe'
    return_to = 'http://localhost:8000'
    return HttpResponseRedirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')
