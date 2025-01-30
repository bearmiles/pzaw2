from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

clubs = {
    "cracovia": {"name": "Cracovia", "logo": "cracovia.png"},
    "gks-katowice": {"name": "GKS Katowice", "logo": "gks.png"},
    "gornik-zabrze": {"name": "Górnik Zabrze", "logo": "gornik.png"},
    "jagiellonia": {"name": "Jagiellonia Białystok", "logo": "jaga.png"},
    "lech-poznan": {"name": "Lech Poznań", "logo": "lech.png"},
    "lechia-gdansk": {"name": "Lechia Gdańsk", "logo": "lechia.png"},
    "legia-warszawa": {"name": "Legia Warszawa", "logo": "legia.png"},
    "motor-lublin": {"name": "Motor Lublin", "logo": "motor.png"},
    "piast-gliwice": {"name": "Piast Gliwice", "logo": "piast.png"},
    "pogon-szczecin": {"name": "Pogoń Szczecin", "logo": "pogon.png"},
}


def index(request):
    return render(request, "social/main.html", {"title": "Ekstraklasa", "clubs": clubs})

def club_detail(request, club_name):
    if club_name in clubs:
        return render(request, "social/club_detail.html", {"title": clubs[club_name]["name"], "club" : clubs[club_name]})
    else:
        return HttpResponse("BŁAD STRONY")
    

