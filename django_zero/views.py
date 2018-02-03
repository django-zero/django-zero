from django.http import HttpResponse


def default_view(request):
    return HttpResponse('Hello, world.')
