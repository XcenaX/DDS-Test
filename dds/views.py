from django.http import JsonResponse
from .models import Category, Subcategory

def get_categories(request):
    type_id = request.GET.get('type_id')
    data = list(Category.objects.filter(type_id=type_id).values('id', 'name'))
    return JsonResponse(data, safe=False)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    data = list(Subcategory.objects.filter(category_id=category_id).values('id', 'name'))
    return JsonResponse(data, safe=False)
