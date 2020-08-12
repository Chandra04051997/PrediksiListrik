from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .bnn import regresi
from .models import data, hasil
import urllib

# Create your views here.
@login_required
def index(request):
    user = User.objects.all()
    datas = data.objects.all()
    hasil = regresi(100,200,4000)
    print(hasil)
    context={
        'title':'Home',
        'dataUser':user,
        'datas':datas,
        'pageTitle':'Dashboard',
        # 'prediksi':bnn()
        'active':'active'
    }
    return render(request, 'index.html', context)

def dataUser(request):
    datas = data.objects.all()
    context={
        'pageTitle':'Data User',
        'active':'active',
        'datas':datas
    }
    return render(request, 'home/userlist.html', context)

class LogoutView(RedirectView):

    url = '/admin/login/?next=/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def create(request):
    x1 = 0
    x2 = 0
    x3 = 0

    if request.method == "POST":
        x1 = int(request.POST['Displacement'])
        x2 = int(request.POST['Horsepower'])
        x3 = int(request.POST['Weight'])
        print(request.POST)
        print(x1)
        print(x2)
        print(x3)
        # id = data.objects.get()
        regresiLinear = regresi(x1,x2,x3)
        print(regresiLinear)

        context = {
            'hasil':regresiLinear,
            'id':id
        }

        return redirect('/data/hasil/?' + urllib.parse.urlencode(context) )
    
    context = {
        'pageTitle':'Create',
    }
    return render(request, 'home/create.html' , context)

def hasil(request, *args, **kwargs):
    if request.method == 'GET':
        context = {
            'hasil':request.GET['hasil'],
            'pageTitle':'Hasil'
        }
        return render(request, 'home/hasil.html', context)