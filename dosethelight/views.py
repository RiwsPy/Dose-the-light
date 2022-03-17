from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
import os
from .settings import BASE_DIR

CITY_NAMES_CHOICE = {
    'seyssinet-pariset': 38170,
    'seyssinet pariset': 38170,
}

ROOT_IMG = 'static/img/'

CITY_DATA = [
    {'name': 'Seyssinet-Pariset',
     'postal_code': 38170},
    {'name': 'Grenoble',
     'postal_code': 38000},
]

# auto-completion imagefile
for city in CITY_DATA:
    if 'imgname' not in city and 'postal_code' in city:
        root_img = ROOT_IMG + str(city['postal_code']) + '_apercu.png'
        if os.path.exists(os.path.join(BASE_DIR, root_img)):
            city['imgname'] = root_img


def home(request: WSGIRequest, *args) -> HttpResponse:
    error_msg = ''
    user_search_postal_code = 0
    if request.method == 'GET':
        user_search = request.GET.get('user_search', '')

        if not user_search or args:
            return render(request,
                          'templates/layouts/base.html',
                          context={
                              'msgs': args,
                              'cities': CITY_DATA,
                          })

        user_search = request.GET.get('user_search', '')
        try:
            user_search_postal_code = int(user_search)
        except ValueError:
            if user_search.lower() in CITY_NAMES_CHOICE:
                user_search_postal_code = CITY_NAMES_CHOICE[user_search.lower()]
            else:
                error_msg = 'Ville non reconnue.'
        else:
            if user_search_postal_code not in CITY_NAMES_CHOICE.values():
                error_msg = 'Code postal non reconnu.'
    else:
        error_msg = 'Méthode non autorisée.'

    if error_msg:
        return home(request, error_msg)

    return redirect('maps', user_search_postal_code)
