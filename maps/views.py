from django.shortcuts import render
from maps.models import influencers_queryset, conflicts_queryset
from django.http import JsonResponse
from entities.time import date_check, date_percent_in_week
import timeit
import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    layer_date = 'We 08:00'
    date_percent = date_percent_in_week(layer_date)

    return render(request,
                  'maps/home.html',
                  context={
                    'layer_date': layer_date,
                    'timecontrol_position': str(date_percent*2)})


def monday_conflicts(request):
    if request.method != 'GET':
        return home(request)



def show_conflicts(request, user_date):
    if request.method != 'GET':
        return home(request)

    debut = timeit.default_timer()
    try:
        user_date = date_check(user_date)
    except AttributeError:
        # error format date
        return home(request)

    # TODO: save this and use it for each request
    int_to_node = {
        conflict.pk: conflict
        for conflict in conflicts_queryset()}
    print('create dict int to id', timeit.default_timer()-debut)

    with open(os.path.join(BASE_DIR, 'db/influ_conflicts.json'), 'r') as file:
        shop_and_conflict_in_range = json.load(file)
    print('load influ conflicts', timeit.default_timer()-debut)
    # TODO: end

    features = set()
    open_shops = 0
    for node in influencers_queryset():
        coef = node.coef_rush(user_date)
        if coef <= 0:
            continue
        open_shops += 1
        for conflict in shop_and_conflict_in_range[str(node.pk)]:
            conflict_id = int_to_node[conflict]
            if conflict_id.is_open(user_date):
                conflict_id.conflicts_value += coef
                # conflict_id.conflicts_details += '\n' + node.name
                features.add(conflict_id)

    print(open_shops, 'shops ouverts')
    print('add_shops', timeit.default_timer()-debut)

    print('fin', timeit.default_timer()-debut)
    print('ok', len(features))
    return JsonResponse({'features': [node.pr_dict
                                      for node in features]})
