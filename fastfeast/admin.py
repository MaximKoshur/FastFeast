from django.contrib import admin
from .models import Dishes, CategoryDishes, CategoryInstitution, Institution

admin.site.register(CategoryInstitution)
admin.site.register(Institution)


@admin.register(Dishes)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "institution")


class ChildrenInline(admin.TabularInline):
    model = CategoryDishes
    fk_name = 'parent'
    extra = 1


class CategoryDishesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    inlines = [ChildrenInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(parent__isnull=True).order_by('name')
        return qs


admin.site.register(CategoryDishes, CategoryDishesAdmin)



