from django.shortcuts import render
from .models import Game


# Create your views here.
def homepage(request):
    return render(request=request, 
                  template_name="main/home.html",
                  context={"games": Game.objects.all})

                  