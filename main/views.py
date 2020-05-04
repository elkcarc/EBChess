from django.shortcuts import render, redirect
from .models import Game, Challenge, Active, Ai
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, ChallengeForm
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
import numpy as np


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
                messages.error(request, "Error Creating User")              
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

def challenges_issue(request):
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            opponent = form.cleaned_data.get('opponent')
            message = form.cleaned_data.get('message')
            #commented for testing purposes
            #if opponent == request.user.username:
            #    messages.error(request, f"You cannot challenge yourself")
            #    return redirect("main:homepage")
            new_challenge_obj = Challenge(challenge_user1=request.user.username,
                                          challenge_user2=opponent,
                                          challenge_issued=datetime.now(),
                                          challenge_message=message)
            new_challenge_obj.save()
            messages.info(request, f"Sent Challenge to {opponent}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}")
    form = ChallengeForm
    return render(request=request,
                  template_name="main/issue.html",
                  context={"form":form})

def challenges_accept(request, challenge_slug):
    for c in Challenge.objects.all():
        if str(c.pk) == str(challenge_slug):
            challenge = c
    if challenge != -1 and request.user.username == challenge.challenge_user2:
        if np.random.random_sample() > 0.5:
            new_active_obj = Active(user1=challenge.challenge_user1,
                                    user2=request.user.username,
                                    last_move=datetime.now(),
                                    active_content="",
                                    active_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        else:
            new_active_obj = Active(user1=request.user.username,
                                    user2=challenge.challenge_user1,
                                    last_move=datetime.now(),
                                    active_content="",
                                    active_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        new_active_obj.save()
        messages.info(request, f"Accepted Challenge from {challenge.challenge_user1}")
        instance = Challenge.objects.get(challenge_id=challenge.challenge_id)
        instance.delete()
        return redirect("main:homepage")

def challenges_decline(request, challenge_slug):
    for c in Challenge.objects.all():
        if str(c.pk) == str(challenge_slug):
            challenge = c
    if challenge != -1 and request.user.username == challenge.challenge_user2:
        instance = Challenge.objects.get(challenge_id=challenge.challenge_id)
        instance.delete()
        messages.info(request, f"Successflly declined the challenge")
        return redirect("main:homepage")

def challenges_request(request):
    challenges = []
    for c in Challenge.objects.all():
        if c.challenge_user2 == request.user.username:
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
        if a.user1 == request.user.username or a.user2 == request.user.username:
            active.append(a)
    noactivefound = True
    if len(active) > 1:
        noactivefound = False
    return render(request=request,
                  template_name="main/active.html",
                  context={"active": active,
                           "noactivefound" : noactivefound})

def active_slug_resign(request, active_slug):
    for a in Active.objects.all():
        if str(a.pk) == str(active_slug):
            active = a
    if active != -1 and (request.user.username == active.user1 or request.user.username == active.user2):
        if request.user.username == active.user1:
            result = "0-1"
        else:
            result = "1-0"
        new_game_obj = Game(game_event="No Event",
                            game_site="On-line",
                            game_published=datetime.now(),
                            game_round="1",
                            game_white=active.user1,
                            game_black=active.user2,
                            game_result=result,
                            game_content=active.active_content,
                            game_fen=active.active_fen)
        new_game_obj.save()
        if request.user.username == active.user1:
            messages.info(request, f"Resigned game against {active.user2}")
        else:
            messages.info(request, f"Resigned game against {active.user1}")
        instance = Active.objects.get(active_id=active.active_id)
        instance.delete()
        return redirect("main:homepage")

def active_slug(request, active_slug):
    for a in Active.objects.all():
        if str(a.pk) == str(active_slug):
            active = a
    if active != -1:
        return render(request=request,
                      template_name="main/activegame.html",
                      context={"active": active})

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
                  
def study_request(request):
    return render(request=request,
                  template_name="main/study.html",
                  context={})

def local_request(request):
    return render(request=request,
                  template_name="main/local.html",
                  context={})

def single_slug(request, single_slug):
    for g in Game.objects.all():
        if str(g.pk) == str(single_slug):
            game = g
    if game != -1:
        return render(request=request,
                      template_name="main/game.html",
                      context={"game": game})

