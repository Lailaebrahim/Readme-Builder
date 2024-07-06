from django.template import loader
from django.http import HttpResponse


def home(request):
    template = loader.get_template('ReadmeBuilderWebApp0/base.html')
    return HttpResponse(template.render(context={}, request=request))


def about(request):
    return HttpResponse("Hello, world From Readme Writter about!")
