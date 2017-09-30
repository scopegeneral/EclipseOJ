from django.shortcuts import render
from django.http import HttpResponse
#from django.template import loader
from django.contrib.auth.models import User
from django.http import Http404
# Create your views here.

def index(request):
    #return HttpResponse("<h1>Yo i'll probably put list of users here</h1>")
    all_users = User.objects.all()
    #template = loader.get_template('profiles/index.html') no bro we'll use shortcut
    context = {'all_users': all_users }  #context is a dictionary here!!!
    return render(request, 'profiles/index.html', context)

def detail(request,nickname):
    #return HttpResponse("<p>I have to display about user " + str(nickname) + "</p>")
    try:
        user = User.objects.get(username=nickname)
    except User.DoesNotExist:
        raise Http404("There is no such username :/ Please check again :P")
    return render(request, 'profiles/detail.html', { 'user': user })
