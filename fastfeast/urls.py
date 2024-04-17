from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'fastfeast'

urlpatterns = [
    path('', views.main, name='main'),
    path('profile/', views.profile_page, name="profile"),
    path('registration/', views.Registration.as_view(), name="registration"),
    path('login/', LoginView.as_view(template_name='fastfeast/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dishes/<int:dish_id>', views.dishes_detail, name='dishes_detail'),
    path('category_dishes/<int:category_id>', views.category_dishes_detail, name='category_dishes_detail'),
    path('category_institutions/<int:category_id>', views.category_institutions_detail, name='category_institutions_detail'),
    path('institution/<int:institution_id>', views.institution_detail, name='institution_detail'),
    path('completed_order', views.completed_order, name='completed_order'),
    path('change_count', views.change_count, name='change_count'),
    path('del_from_cart', views.del_from_cart, name='del_from_cart'),
    path('add_to_cart', views.add_to_cart, name="add_to_cart"),
]
