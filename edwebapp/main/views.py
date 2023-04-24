from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>start project</h1>')
