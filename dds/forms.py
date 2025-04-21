from django import forms
from .models import Transaction, Category, Subcategory

class TransactionForm(forms.ModelForm):
    """
    Форма для модели Transaction с динамическим изменением доступных значений полей
    'category' и 'subcategory' в зависимости от выбранного типа транзакции.
    При выборе типа автоматически фильтруются категории, а при выборе категории — подкатегории.
    Это позволяет пользователю выбирать только логически связанные значения,
    соблюдая иерархию: Тип → Категория → Подкатегория.
    """
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)

        if 'category' in self.data:
            try:
                cat_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=cat_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
