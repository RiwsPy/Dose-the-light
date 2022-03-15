from django.shortcuts import redirect, render
from django.urls.base import reverse
from maps.models import influencers_queryset, conflicts_queryset
from django.http import JsonResponse
from entities.time import date_check
import timeit
import json
from pathlib import Path
import os
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse

BASE_DIR = Path(__file__).resolve().parent.parent


def show_map(request, postal_code: int = 38170):
    return render(request,
                  'maps/map.html',
                  context={'postal_code': postal_code})


def show_json(request, filename: str):
    print(filename)
    with open(os.path.join(BASE_DIR, f'db/{filename}'), 'r') as file:
        return JsonResponse(json.load(file))


days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

conflicts_hour = dict()

with open(os.path.join(BASE_DIR, 'db/influ_conflicts.json'), 'r') as file:
    shop_and_conflict_in_range = json.load(file)


def show_conflicts(request, user_date):
    if request.method != 'GET':
        return show_map(request)

    nb_hour = user_date // 3600000
    nb_day = nb_hour // 24
    nb_hour -= nb_day*24
    user_date = f'{days[nb_day]} {str(nb_hour).zfill(2)}:00'
    print(user_date)

    debut = timeit.default_timer()
    try:
        user_date_check = date_check(user_date)
    except AttributeError:
        # error format date
        return show_map(request)

    # TODO: save this and use it for each request
    int_to_node = {
        conflict.pk: conflict
        for conflict in conflicts_queryset()}
    # TODO: end

    features = set()
    open_shops = 0
    for node in influencers_queryset():
        coef = node.coef_rush(user_date_check)
        if coef <= 0:
            continue
        open_shops += 1
        for conflict in shop_and_conflict_in_range[str(node.pk)]:
            conflict_id = int_to_node[conflict]
            if conflict_id.is_open(user_date_check):
                conflict_id.conflicts_value += coef
                # conflict_id.conflicts_details += '\n' + node.name
                features.add(conflict_id)

    print(open_shops, 'shops ouverts')
    #print('add_shops', timeit.default_timer()-debut)

    #print('fin', timeit.default_timer()-debut)
    #print('ok', len(features))

    return JsonResponse({'features': [node.pr_dict
                        for node in features]})


def redirect_last_page_or_home(request: WSGIRequest) -> HttpResponse:
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))


def go_home(request: WSGIRequest, *args) -> HttpResponse:
    return render(request, 'templates/layouts/base.html', context={'msgs': args})
