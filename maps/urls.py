from django.urls import path
from django.views.generic import TemplateView
from .views import home, show_conflicts

urlpatterns = [
    path('', home, name='maps'),
    path('api/<str:user_date>', show_conflicts, name='show_conflicts'),
    path('umap/', TemplateView.as_view(template_name='maps/test_umap.html'), name='umap')
]
