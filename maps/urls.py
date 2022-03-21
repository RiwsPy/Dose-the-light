from django.urls import path
from django.views.generic import TemplateView
from .views import show_map, show_json, show_conflicts

urlpatterns = [
    path('', show_map, name='maps'),
    path('api/file/<str:filename>', show_json, name='show_json'),
    path('api/date/<int:user_date>', show_conflicts, name='show_conflicts')
]
