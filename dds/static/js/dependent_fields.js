(function($) {
    $(document).ready(function() {
        // поля формы
        const $type = $('#id_type');
        const $category = $('#id_category');
        const $subcategory = $('#id_subcategory');

        const initialType = $type.val();
        const initialCategory = $category.val();
        const initialSubcategory = $subcategory.val();

        // ID запросов, чтобы не было дубликатов
        let currentCategoryRequestId = 0;
        let currentSubcategoryRequestId = 0;

        // Обновление списка категорий на основе выбранного типа
        function updateCategories(typeId, selectedCategoryId = null) {
            const currentValue = $category.val();
            const thisRequestId = ++currentCategoryRequestId;

            // Очищаем категории и подкатегории
            $category.empty().append('<option value="">---------</option>');
            $subcategory.empty().append('<option value="">---------</option>');

            if (!typeId) return;

            // Загружаем категории по выбранному типу
            $.getJSON("/dds/ajax/categories/", { type_id: typeId }, function(data) {
                // Проверяем, не устарел ли запрос
                if (thisRequestId !== currentCategoryRequestId) return;

                // Добавляем полученные категории
                $.each(data, function(index, item) {
                    const selected = (item.id == currentValue) ? 'selected' : '';
                    $category.append(`<option value="${item.id}" ${selected}>${item.name}</option>`);
                });

                // Если была выбрана категория — подгружаем подкатегории
                if (currentValue) {
                    updateSubcategories(currentValue, initialSubcategory);
                }
            });
        }

        // Обновление списка подкатегорий на основе выбранной категории
        function updateSubcategories(categoryId, selectedSubcategoryId = null) {
            const thisRequestId = ++currentSubcategoryRequestId;

            // Очищаем подкатегории
            $subcategory.empty().append('<option value="">---------</option>');

            if (!categoryId) return;

            // Загружаем подкатегории по выбранной категории
            $.getJSON("/dds/ajax/subcategories/", { category_id: categoryId }, function(data) {
                if (thisRequestId !== currentSubcategoryRequestId) return;

                // Добавляем полученные подкатегории
                $.each(data, function(index, item) {
                    const selected = (item.id == selectedSubcategoryId) ? 'selected' : '';
                    $subcategory.append(`<option value="${item.id}" ${selected}>${item.name}</option>`);
                });
            });
        }

        // Инициализация: если выбраны значения — заполняем их
        if (initialType) {
            updateCategories(initialType, initialCategory);
        }

        if (!initialCategory) {
            $subcategory.empty().append('<option value="">---------</option>');
        }

        // Сброс селектов при выборе пустого значения
        $type.change(function() {
            const selectedType = $(this).val();
            currentCategoryRequestId++;

            if (!selectedType) {
                $category.empty().append('<option value="">---------</option>');
                $subcategory.empty().append('<option value="">---------</option>');
                return;
            }

            updateCategories(selectedType);
        });

        $category.change(function() {
            const selectedCategory = $(this).val();
            currentSubcategoryRequestId++;

            if (!selectedCategory) {
                $subcategory.empty().append('<option value="">---------</option>');
                return;
            }

            updateSubcategories(selectedCategory);
        });
    });
})(django.jQuery);
