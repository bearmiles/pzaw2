from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template("social/templates/main.html")
    context = {
        "content": "12345"
    }
    return render(request, template,context)