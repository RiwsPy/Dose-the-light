from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from maps.models import City

NB_FAVORITE_CITIES = 3


def home(request: WSGIRequest, *args) -> HttpResponse:
    error_msg = ''

    if request.method == 'GET':
        user_search = request.GET.get('user_search', '')

        if not user_search or args:
            return render(request,
                          'templates/layouts/base.html',
                          context={
                              'msgs': args,
                              'cities': City.objects.all()[:NB_FAVORITE_CITIES],
                          })

        user_search = request.GET.get('user_search', '')
        if user_search.isdigit():
            try:
                user_search_city = City.objects.get(postal_code=int(user_search))
            except ObjectDoesNotExist:
                error_msg = 'Code postal non reconnu.'
        else:
            try:
                user_search_city = City.objects.get(name__iexact=user_search)
            except ObjectDoesNotExist:
                error_msg = 'Ville non reconnue.'
    else:
        error_msg = 'Méthode non autorisée.'

    if error_msg:
        return home(request, error_msg)

    user_search_city.nb_click += 1
    user_search_city.save()
    return redirect('maps', user_search_city.postal_code)
