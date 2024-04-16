from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'fastfeast'

urlpatterns = [
    path('', views.main, name='main'),
    path('dishes/<int:dish_id>', views.dishes_detail, name='dishes_detail'),
    path('category_dishes/<int:category_id>', views.category_dishes_detail, name='category_dishes_detail'),
    path('category_institutions/<int:category_id>', views.category_institutions_detail, name='category_institutions_detail'),
    path('institution/<int:institution_id>', views.institution_detail, name='institution_detail'),

]
