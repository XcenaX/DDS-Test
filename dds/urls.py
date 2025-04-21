from django.urls import path
from . import views

urlpatterns = [
    path('ajax/categories/', views.get_categories, name='ajax_categories'),
    path('ajax/subcategories/', views.get_subcategories, name='ajax_subcategories'),
]
