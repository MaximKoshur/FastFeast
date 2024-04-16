from django.shortcuts import render, get_object_or_404
from .models import Dishes, CategoryDishes, CategoryInstitution, Institution
from .yamaps import generate_yandex_map_basket_html, generate_yandex_map_institution_html


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






