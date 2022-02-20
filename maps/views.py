from django.shortcuts import render
from maps.models import influencers_queryset, conflicts_queryset
from django.http import JsonResponse
from entities.time import date_check
import timeit
import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    return render(request,
                  'maps/home.html')


def show_json(request, filename):
    with open(os.path.join(BASE_DIR, f'db/{filename}'), 'r') as file:
        return JsonResponse(json.load(file))


def monday_conflicts(request):
    if request.method != 'GET':
        return home(request)

    debut = timeit.default_timer()

    # TODO: save this and use it for each request
    int_to_node = {
        conflict.pk: conflict
        for conflict in conflicts_queryset()}
    print('create dict int to id', timeit.default_timer()-debut)

    with open(os.path.join(BASE_DIR, 'db/influ_conflicts.json'), 'r') as file:
        shop_and_conflict_in_range = json.load(file)
    print('load influ conflicts', timeit.default_timer()-debut)
    # TODO: end

    ret = dict({"type": "FeatureCollection", 'features': []})

    for hour in range(24):
        hour_str = '2022-03-01T' + str(hour).zfill(2) + ':00:000Z'
        hour_str_re = date_check(f'Mo {str(hour).zfill(2)}:00')
        features = set()
        for node in influencers_queryset():
            coef = node.coef_rush(hour_str_re)
            if coef <= 0:
                continue
            for conflict in shop_and_conflict_in_range[str(node.pk)]:
                conflict_id = int_to_node[conflict]
                if conflict_id.is_open(hour_str_re):
                    conflict_id.conflicts_value += coef
                    # conflict_id.conflicts_details += '\n' + node.name
                    conflict_id.time = hour_str
                    features.add(conflict_id)

        ret['features'].extend(
            [node.pr_dict
                for node in features]
        )

    print('fin', timeit.default_timer()-debut)
    return JsonResponse(ret)


days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

conflicts_hour = dict()


def show_conflicts(request, user_date):
    if request.method != 'GET':
        return home(request)

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
        return home(request)

    # TODO: save this and use it for each request
    int_to_node = {
        conflict.pk: conflict
        for conflict in conflicts_queryset()}
    #print('create dict int to id', timeit.default_timer()-debut)

    with open(os.path.join(BASE_DIR, 'db/influ_conflicts.json'), 'r') as file:
        shop_and_conflict_in_range = json.load(file)
    #print('load influ conflicts', timeit.default_timer()-debut)
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

    ret = {'features': [node.pr_dict
                        for node in features]}

    return JsonResponse(ret)
