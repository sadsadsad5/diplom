document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort');

    // Обработчик изменения сортировки
    sortSelect.addEventListener('change', function() {
        const sortValue = this.value;
        const url = new URL(window.location.href);
        const searchParams = new URLSearchParams(url.search);

        // Удаляем параметр страницы (чтобы вернуться на 1 страницу)
        searchParams.delete('page');

        // Устанавливаем параметр сортировки
        switch(sortValue) {
            case 'price_asc':
                searchParams.set('sort', 'price');
                break;
            case 'price_desc':
                searchParams.set('sort', '-price');
                break;
            default: // 'newest'
                searchParams.set('sort', '-list_date');
        }

        // Перенаправляем с новыми параметрами
        window.location.search = searchParams.toString();
    });

    // Установка текущего значения из URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentSort = urlParams.get('sort');

    if (currentSort) {
        switch(currentSort) {
            case 'price':
                sortSelect.value = 'price_asc';
                break;
            case '-price':
                sortSelect.value = 'price_desc';
                break;
            case '-list_date':
                sortSelect.value = 'newest';
                break;
        }
    }
});