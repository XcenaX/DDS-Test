from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction
from .forms import TransactionForm

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionForm
    list_display = ['created_at', 'status', 'type', 'category', 'subcategory', 'amount', "comment"]
    list_filter = ['created_at', 'status', 'type', 'category', 'subcategory']
    search_fields = ['comment', "amount"]
    date_hierarchy = 'created_at'

    class Media:
        js = ('admin/js/jquery.init.js', 'js/dependent_fields.js')

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
