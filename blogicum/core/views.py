from django.shortcuts import render


def csrf_failure(request, reason=''):
    """Конструирует представление для ошибки 403."""
    return render(request, 'pages/403csrt.html', status=403)


def page_not_found(request, exception):
    """Конструирует представление для ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def internal_server_error(request):
    """Конструирует представление для ошибки 500."""
    return render(request, 'pages/500.html', status=500)
