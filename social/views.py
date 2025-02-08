from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Comment
from .forms import CommentForm



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

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            pwd = request.POST.get('pwd')
            print(fnm, pwd)
            my_user = User.objects.create_user(username=fnm, password=pwd)
            my_user.save()
            user_model = User.objects.get(username=fnm)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            if my_user is not None:
                login(request, my_user)
                return redirect('/')
            return redirect('/loginn')

        return render(request, 'social/signup.html')


    except Exception as e:
        invalid = "User already exists"
        print("Błąd:", e)
        return render(request, 'social/signup.html', {'invalid': invalid})


def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        invalid="Invalid credentials"
        return render(request,'social/loginn.html', {'invalid': invalid})
    return render(request, 'social/loginn.html')

@login_required(login_url="loginn")
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, "social/main.html", {"title": "Ekstraklasa", "clubs": clubs, "profile": profile, "user": request.user})


@login_required(login_url="loginn")
def club_detail(request, club_name):
    if club_name not in clubs:
        return HttpResponse("BŁĄD STRONY")

    comments = Comment.objects.filter(club=club_name).order_by("-created")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.club = club_name
            comment.save()
            return redirect(f"/club/{club_name}")
    else:
        form = CommentForm()

    return render(request, "social/club_detail.html", {
        "title": clubs[club_name]["name"],
        "club": clubs[club_name],
        "comments": comments,
        "form": form,
    })

@login_required(login_url="loginn")
def logoutt(request):
    logout(request)
    return redirect("/")

