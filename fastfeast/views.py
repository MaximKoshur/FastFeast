from .tasks import change_status
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import Dishes, CategoryDishes, CategoryInstitution, Institution, Order, OrderEntry, Profile
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
        if not profile.shopping_cart or profile.shopping_cart.status in ['DELIVERED', 'PREPARE', 'ONTHEWAY']:
            profile.shopping_cart = Order.objects.create(profile=profile)
            profile.save()
        institutions = [x.dish.institution for x in profile.shopping_cart.order_entries.all()]
        if OrderEntry.objects.filter(order=profile.shopping_cart.id) and (dish.institution not in institutions):
            messages.warning(request, 'Вы не можете добавить блюдо другого ресторана!')
            return redirect('fastfeast:add_to_cart')

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
        if basket:
            lat = profile.shopping_cart.order_entries.first().dish.institution.latitude
            lon = profile.shopping_cart.order_entries.first().dish.institution.longitude
            return render(request, 'fastfeast/add_to_cart.html',
                          {'basket': basket, 'price': profile.shopping_cart.total_price(),
                                   'yamaps': generate_yandex_map_basket_html(request.user.latitude, request.user.longitude, lat, lon)})
        else:
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
        order = profile.shopping_cart
        order.status = 'PREPARE'
        order.save()
        change_status.delay(order.id)
        messages.success(request, 'Your order has been placed!')
        return redirect('fastfeast:add_to_cart')


@login_required
def change_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            profile.user.first_name = first_name
            profile.user.save()
        if 'last_name' in request.POST:
            last_name = request.POST['last_name']
            profile.user.last_name = last_name
            profile.user.save()
        if 'email' in request.POST:
            email = request.POST['email']
            profile.user.email = email
            profile.user.save()
        if 'address' in request.POST:
            address = request.POST['address']
            profile.user.address = address
            profile.user.save()
        return redirect('fastfeast:profile')


@login_required
def orders_history(request, page_number=1):
    profile = Profile.objects.get(user=request.user)
    completed_orders = Paginator(Order.objects.filter(status='DELIVERED', profile=profile).order_by('-id')[:5], 3)
    page_obj = completed_orders.get_page(page_number)
    return render(request, 'fastfeast/orders_history.html', {'context': completed_orders, 'orders': page_obj})


@login_required
def repeat_order(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.get(id=order_id, profile=profile)
        new_order = Order.objects.create(profile=profile, status='INPROGRESS')
        order_entries = OrderEntry.objects.filter(order=order)
        for entry in order_entries:
            OrderEntry.objects.create(order=new_order, dish=entry.dish, count=entry.count)
        profile.shopping_cart = new_order
        profile.save()
        return redirect('fastfeast:add_to_cart')
