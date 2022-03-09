from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
POSTAL_CODES = (38170, 38000)
CITY_NAMES = {
    'seyssinet-pariset': 38170,
    'seyssinet pariset': 38170,
}


def home(request: WSGIRequest) -> HttpResponse:
    return render(request, 'templates/layouts/base.html')


def home_with_msgs(request: WSGIRequest, *args) -> HttpResponse:
    return render(request, 'templates/layouts/base.html', context={'msgs': args})


def result(request: WSGIRequest) -> HttpResponse:
    if request.method != 'GET':
        return home_with_msgs(request, 'Méthode non autorisée.')

    user_search = request.GET.get('user_search', '')
    try:
        user_search_int = int(user_search)
    except ValueError:
        if user_search.lower() in CITY_NAMES:
            return redirect('maps', CITY_NAMES[user_search.lower()])
        return home_with_msgs(request, 'Ville non reconnue.')
    else:
        if user_search_int in POSTAL_CODES:
            return redirect('maps', user_search)

    return home_with_msgs(request, 'Code postal non reconnu.')
