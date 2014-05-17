from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def edhome(request):
    return render(request, 'edhome.html')

def edhome_new(request):
    return render(request, 'edhome_new.html')


def login(request):
    return HttpResponse('Login!')

def logout(request):
    return HttpResponse('Logout!')