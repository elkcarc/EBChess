from django.shortcuts import render, redirect
from .models import Game, Challenge, Active, Ai
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.http import HttpResponse


# Create your views here.

def homepage(request):
    games = []
    for g in Game.objects.all():
        games.append(g)
    games = reversed(games)
    return render(request=request, 
                  template_name="main/home.html",
                  context={"games": games})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Registration Successful!")
            login(request, user) 
            messages.info(request, f"Logged in as {username}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}")
                
    form = NewUserForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Logged in as {username}")
                    return redirect("main:homepage")
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request=request, 
                  template_name="main/login.html",
                  context={"form":form})
                  
def account_request(request):
    games = []
    for g in Game.objects.all():
        if g.game_white == request.user.username or g.game_black == request.user.username:
            games.append(g)
    nogamesfound = True
    if len(games) > 1:
        nogamesfound = False
    return render(request=request,
                  template_name="main/account.html",
                  context={"games": games,
                           "nogamesfound" : nogamesfound})

def challenges_request(request):
    challenges = []
    for c in Challenge.objects.all():
        if c.challenge_user1 == request.user.username or c.challenge_user1 == request.user.username:
            challenges.append(c)
    nochallengesfound = True
    if len(challenges) > 1:
        nochallengesfound = False
    return render(request=request,
                  template_name="main/challenges.html",
                  context={"challenges": challenges,
                           "nochallengesfound" : nochallengesfound})

def active_request(request):
    active = []
    for a in Active.objects.all():
        if a.user1 == request.user.username or a.user1 == request.user.username:
            active.append(a)
    noactivefound = True
    if len(active) > 1:
        noactivefound = False
    return render(request=request,
                  template_name="main/active.html",
                  context={"active": active,
                           "noactivefound" : noactivefound})

def ai_request(request):
    ai = []
    for a in Ai.objects.all():
        if a.user == request.user.username:
            ai.append(a)
    noaifound = True
    if len(ai) > 1:
        noaifound = False
    return render(request=request,
                  template_name="main/ai.html",
                  context={"ai": ai,
                           "noaifound" : noaifound})
                  
def single_slug(request, single_slug):
    for g in Game.objects.all():
        if str(g.pk) == str(single_slug):
            game = g
    if game != -1:
        return render(request=request,
                      template_name="main/game.html",
                      context={"game": game})
