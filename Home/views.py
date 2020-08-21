from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, ListView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .bnn import regresi
from .models import data, hasil, datasCSV
import urllib
import csv, io
from django.contrib import messages
from .forms import FileForm
from django.http import HttpResponseRedirect
import pandas as pd
from django.db import connection
from django.core.files.storage import FileSystemStorage
from .forms import FileForm


# Create your views here.
@login_required
def index(request):
    user = User.objects.all()
    datas = datasCSV.objects.all()
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

def uploadCSV(request):
    dataCSVs = datasCSV.objects.all()

    if request.method == "POST":
        csv_file = request.FILES['file']
        print(csv_file.name)
        print("aaa")
        form = FileForm(request.FILES)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return HttpResponseRedirect(reverse('home:csvlist'))
        else:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)

            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                created = datasCSV.objects.create(
                    nama_tahun = column[0],
                    data_content = column[1],
                )
            if form.is_valid():
                form.save()

            return HttpResponseRedirect(reverse('home:csvlist'))
    else:
        form = FileForm(request.POST, request.FILES)
        context = {
            'pageTitle':'uploadCSV',
            'form':form
        }

        return render(request,'home/uploadCSV.html', context)

class CSVListView(ListView):
    template_name = 'home/csvlist.html'
    model = datasCSV
    extra_context = {
        'pageTitle':'List'
    }
    def get_queryset(self):
        queryset = str(self.model.objects.all().query)
        df = pd.read_sql_query(queryset, connection)
        df.nama_tahun = pd.to_datetime(df.nama_tahun)
        df = df.set_index('nama_tahun')
        print(df[['data_content']])
        return super().get_queryset()

def deleteAll(request):
    dataCSV.objects.all().delete()
    return HttpResponseRedirect(reverse('home:csvlist'))