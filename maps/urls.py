from django.urls import path
from django.views.generic import TemplateView
from .views import home, show_json, monday_conflicts, show_conflicts

urlpatterns = [
    path('', home, name='maps'),
    path('api/<str:filename>', show_json, name='show_json'),
    path('monday/', monday_conflicts, name='monday_conflicts'),
    path('api/date/<int:user_date>', show_conflicts, name='show_conflicts')
]
