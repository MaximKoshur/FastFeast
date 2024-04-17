from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import Dishes, CategoryDishes, CategoryInstitution, Institution, CustomUser, Order, OrderEntry, Profile
from .yamaps import generate_yandex_map_basket_html, generate_yandex_map_institution_html
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required


class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('address',)


class Registration(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("fastfeast:main")
    template_name = "fastfeast/registration.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('fastfeast:main')
    else:
        return render(request, 'fastfeast/login.html')


def logout_view(request):
    logout(request)
    return redirect('fastfeast:main')


def main(request):
    context = {"institutions": Institution.objects.all(),
               "categories_institutions": CategoryInstitution.objects.all(),
               "categories_dishes": CategoryDishes.objects.filter(parent=None)
               }
    return render(request, 'fastfeast/main.html', context)


def dishes_detail(request, dish_id: int):
    context = {'dish': get_object_or_404(Dishes, id=dish_id)}
    return render(request, 'fastfeast/dishes_detail.html', context)


def institution_detail(request, institution_id: int):
    i = get_object_or_404(Institution, id=institution_id)
    context = {'institution': i,
               'dishes': Dishes.objects.filter(institution=i),
               'yamaps': generate_yandex_map_institution_html(i.latitude, i.longitude)}
    return render(request, 'fastfeast/institution_detail.html', context)


def category_dishes_detail(request, category_id: int):
    c = get_object_or_404(CategoryDishes, id=category_id)
    if c.parent is None:
        context = {'category': c,
                   'sub_category': CategoryDishes.objects.filter(parent=category_id)}
        return render(request, 'fastfeast/category_dishes_detail.html', context)
    else:
        context = {'category': c,
                   'dishes': Dishes.objects.filter(category=category_id)}
        return render(request, 'fastfeast/category_dishes_detail.html', context)


def category_institutions_detail(request, category_id: int):
    context = {'category': get_object_or_404(CategoryInstitution, id=category_id),
               'institutions': Institution.objects.filter(category=get_object_or_404(CategoryInstitution, id=category_id))}
    return render(request, 'fastfeast/category_institutions_detail.html', context)


@login_required
def profile_page(request):
    try:
        profile = get_object_or_404(Profile, user=request.user)
    except:
        profile = Profile.objects.create(user=request.user)
    context = {'profile': profile, }
    return render(request, 'fastfeast/profile.html', context)


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        dish_id = request.POST['id']
        dish = get_object_or_404(Dishes, id=dish_id)
        try:
            profile = get_object_or_404(Profile, user=request.user)
        except:
            profile = Profile.objects.create(user=request.user)
        if not profile.shopping_cart or profile.shopping_cart.status == 'DELIVERED':
            profile.shopping_cart = Order.objects.create(profile=profile)
            profile.save()
        try:
            order_entry = get_object_or_404(OrderEntry, order=profile.shopping_cart, dish=dish)
        except:
            order_entry = OrderEntry.objects.create(order=profile.shopping_cart, dish=dish)
        order_entry.count += 1
        order_entry.save()
        return redirect('fastfeast:dishes_detail', dish_id=dish_id)
    else:
        try:
            profile = get_object_or_404(Profile, user=request.user)
        except:
            profile = Profile.objects.create(user=request.user)
        if not profile.shopping_cart:
            profile.shopping_cart = Order.objects.create(profile=profile)
            profile.save()
        basket = OrderEntry.objects.filter(order=profile.shopping_cart, order__status='INPROGRESS')
        return render(request, 'fastfeast/add_to_cart.html',
                      {'basket': basket, 'price': profile.shopping_cart.total_price()})


@login_required
def del_from_cart(request):
    if request.method == 'POST':
        dish_ids = request.POST.getlist('dish_id')
        profile = Profile.objects.get(user=request.user)
        for dish_id in dish_ids:
            dish = get_object_or_404(Dishes, id=dish_id)
            OrderEntry.objects.filter(order=profile.shopping_cart, dish=dish).delete()
            profile.shopping_cart.save()
        return redirect('fastfeast:add_to_cart')


@login_required
def change_count(request):
    if request.method == 'POST':
        dish_id = request.POST['dish_id']
        count = int(request.POST['count'])
        profile = Profile.objects.get(user=request.user)
        dish = get_object_or_404(Dishes, id=dish_id)
        if count == 0:
            OrderEntry.objects.filter(order=profile.shopping_cart, dish=dish).delete()
            profile.shopping_cart.save()
            return redirect('fastfeast:add_to_cart')
        order_entry = OrderEntry.objects.get(order=profile.shopping_cart, dish=dish)
        order_entry.count = count
        order_entry.save()
        profile.shopping_cart.save()
        return redirect('fastfeast:add_to_cart')


@login_required
def completed_order(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.shopping_cart.status = 'PREPARE'
        profile.shopping_cart.save()
        messages.success(request, 'Your order has been placed!')
        return redirect('fastfeast:add_to_cart')
