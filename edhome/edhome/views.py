from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def edhome(request):
    #poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'edhome.html')


def login(request):
    return HttpResponse('Login!')

def logout(request):
    return HttpResponse('Logout!')