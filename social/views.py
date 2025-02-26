from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Comment
from .forms import CommentForm



clubs = {
    "cracovia": {"name": "Cracovia", "logo": "cracovia.png", "history" : """
    Cracovia to jeden z najstarszych klubów piłkarskich w Polsce, założony w 1906 roku w Krakowie.
    Zespół zdobył dwukrotnie mistrzostwo Polski (1948, 2021) oraz sześć razy Puchar Polski.
    Cracovia, mimo długiej historii, przez wiele lat nie należała do czołówki polskiej piłki,
    ale w ostatnich latach znacząco poprawiła swoją formę, walcząc o najwyższe lokaty w Ekstraklasie.
    Kibice „Pasów” są znani z ogromnej pasji i oddania,
    a rywalizacja z Wisłą Kraków, czyli „święta wojna”, to jedno z najgorętszych wydarzeń w polskim futbolu.
    Cracovia to klub z bogatą tradycją, którego historia sięga ponad 100 lat,
    i którego znaczenie dla Krakowa i polskiej piłki jest nieocenione.
 """},
    "gks-katowice": {"name": "GKS Katowice", "logo": "gks.png", "history" : """
    Górnik Katowice, choć obecnie gra w niższych ligach, to ma bogatą historię w polskim futbolu.
    Klub został założony w 1964 roku, a swoje największe sukcesy odnosił w latach 80.
    XX wieku, kiedy to dwukrotnie zdobył Puchar Polski (1986, 1991) i regularnie rywalizował w europejskich pucharach.
    Górnik Katowice przez wiele lat był solidnym przedstawicielem Śląska w Ekstraklasie
    , a jego kibice są znani z oddania i pasji do drużyny.
    Choć klub borykał się z trudnościami finansowymi i spadkami do niższych lig,
    nadal jest jednym z bardziej rozpoznawalnych klubów w regionie. Górnik Katowice,
    mimo mniejszych sukcesów w ostatnich latach, wciąż jest symbolem miasta i ma wierną rzeszę fanów
    , którzy pamiętają jego najlepsze lata.
    Klub stawia na młodych zawodników i odbudowę swojej pozycji w polskim futbolu.              
                     
    """},
    "gornik-zabrze": {"name": "Górnik Zabrze", "logo": "gornik.png", "history" : """
        Górnik Zabrze, założony w 1948 roku, to jeden z najbardziej utytułowanych klubów w Polsce.
        Klub z Zabrza zdobył czternaście tytułów mistrza Polski, a także sześć Pucharów Polski,
        co czyni go jednym z najbardziej utytułowanych w kraju. Największe sukcesy odnosił w latach 60. i 80.,
        kiedy to dominował na krajowych boiskach i regularnie występował w europejskich pucharach.
        Górnik jest również symbolem Śląska i ma wierną rzeszę kibiców,
        którzy przez lata wspierali drużynę.              
        """},
    "jagiellonia": {"name": "Jagiellonia Białystok", "logo": "jaga.png", "history" : """
        Jagiellonia Białystok, założona w 1920 roku, to klub, który w ostatnich latach zdołał przebić się do czołówki polskiej piłki. 
        Jagiellonia trzykrotnie zajmowała drugie miejsce w Ekstraklasie,
        a także regularnie walczy o europejskie puchary.
        Dzięki wsparciu swoich wiernych kibiców z Białegostoku,
        klub zdołał stworzyć silną drużynę, która potrafi rywalizować z najlepszymi.            
    """},
    "lech-poznan": {"name": "Lech Poznań", "logo": "lech.png", "history" : """
     Lech Poznań, założony w 1922 roku, to klub, który zyskał sobie miano jednego z najlepszych w Polsce.
    „Kolejorz” zdobył cztery tytuły mistrza Polski i sześć Pucharów Polski. 
    Zespół z Poznania jest regularnym uczestnikiem europejskich pucharów, gdzie wielokrotnie walczył z najlepszymi drużynami Europy.
    Legendarni zawodnicy, tacy jak Piotr Reiss czy Jakub Moder, wpisały się na stałe w historię klubu.
    Kibice Lecha są uznawani za jednych z najbardziej oddanych w Polsce.                                 
    """},
    "lechia-gdansk": {"name": "Lechia Gdańsk", "logo": "lechia.png", "history" : """
    Lechia Gdańsk, założona w 1945 roku, ma na swoim koncie kilka ważnych sukcesów,
    w tym Puchar Polski w 1983 roku oraz regularne występy w europejskich pucharach.
    Klub z Trójmiasta stawia na rozwój infrastruktury i wychowanie młodych piłkarzy.
    Kibice Lechii są uważani za jednych z najbardziej zaangażowanych i pasjonujących w Polsce.                            
    """},
    "legia-warszawa": {"name": "Legia Warszawa", "logo": "legia.png", "history" : """
        Legia Warszawa, klub powstały w 1916 roku, to jeden z najstarszych i najbardziej utytułowanych klubów piłkarskich w Polsce.
    Legia zdobyła aż 15 tytułów mistrza Polski oraz 19 Pucharów Polski, co czyni ją dominującą drużyną w historii krajowego futbolu. 
    Klub wielokrotnie rywalizował w europejskich pucharach, 
    a jego kibice, znani z licznych i głośnych opraw, stanowią jedną z najliczniejszych grup fanów w Polsce.
    Legia to również klub, który regularnie dostarcza reprezentacji Polski utalentowanych zawodników.                               
    """},
    "motor-lublin": {"name": "Motor Lublin", "logo": "motor.png", "history" : """
        Motor Lublin to klub piłkarski założony w 1944 roku, który ma długą historię, 
        choć nie należy do czołówki polskiego futbolu. Motor przez wiele lat rywalizował głównie w niższych ligach, 
        ale w ostatnich dekadach kilkakrotnie grał w Ekstraklasie, 
        choć nie odnosił większych sukcesów na najwyższym poziomie. 
        Największym osiągnięciem klubu była gra w pierwszej lidze, 
        a w latach 70. i 80. XX wieku, Motor Lublin cieszył się większymi sukcesami,
        zdobywając między innymi Puchar Polski w 1975 roku.

        Kibice Motoru są znani z dużego zaangażowania i tworzą świetną atmosferę na meczach,
        mimo że klub nie odnosił sukcesów na miarę największych drużyn w Polsce.
        Motor Lublin to także klub z dużą tradycją w regionie Lubelszczyzny,
        który obecnie stara się wrócić do najwyższych lig. Choć nie zdobywał wielu tytułów,
        klub ma wielu wiernych fanów, którzy wciąż liczą na powrót drużyny do ekstraklasy
        i osiąganie wyższych celów.                           
    """},
    "piast-gliwice": {"name": "Piast Gliwice", "logo": "piast.png", "history" : """                    
        Piast Gliwice, choć stosunkowo młody klub, 
        założony w 1945 roku, zdobył swoje pierwsze mistrzostwo Polski dopiero w 2015 roku.
        To sukces, który zapisał się w historii polskiej piłki nożnej, 
        ponieważ Piast stał się jednym z najmłodszych mistrzów Polski. Klub regularnie rywalizuje w europejskich pucharach,
        a jego kibice są znani z ogromnej pasji i oddania drużynie. 
        Piast to przykład, że determinacja i ciężka praca mogą prowadzić do sukcesu,
        nawet jeśli klub nie ma takiej tradycji jak niektóre starsze drużyny.                                    
    """},
    "pogon-szczecin": {"name": "Pogoń Szczecin", "logo": "pogon.png", "history" : """
    Pogoń Szczecin, założona w 1948 roku, to jeden z ważniejszych klubów w Polsce, 
    choć nigdy nie zdobył mistrzostwa kraju.
    Pogoń regularnie rywalizuje o najwyższe lokaty w Ekstraklasie i ma duże ambicje. 
    Kibice Pogoni są znani ze swojego oddania drużynie,
    a stadion w Szczecinie regularnie wypełnia się tłumem kibiców.                                          
"""},
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

