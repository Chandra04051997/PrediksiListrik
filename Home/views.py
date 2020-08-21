from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
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

from django.db import connection
from django.core.files.storage import FileSystemStorage
from .forms import FileForm
# Neural Network Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
from statsmodels.tools.eval_measures import rmse
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from pandas.tseries.offsets import DateOffset
import warnings
import urllib, base64


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

    def get_context_data(self,*args, **kwargs):
        queryset = str(self.model.objects.all().query)
        df = pd.read_sql_query(queryset, connection)
        df.nama_tahun = pd.to_datetime(df.nama_tahun)
        df = df.set_index('nama_tahun')
        plt.figure(figsize=(20, 5))
        plt.plot(df.index, df['data_content'])
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        self.kwargs.update({'matplot':uri})
        kwargs = self.kwargs
        return super().get_context_data(*args, **kwargs)
    

def deleteAll(request):
    dataCSV.objects.all().delete()
    return HttpResponseRedirect(reverse('home:csvlist'))

def trainData(request):
        queryset = str(datasCSV.objects.all().query)
        df = pd.read_sql_query(queryset, connection)
        df.nama_tahun = pd.to_datetime(df.nama_tahun)
        df = df.set_index('nama_tahun')
        print(df[['data_content']])

        df2 = df[['data_content']]
        train, test = df2[:-12], df2[-12:]

        scaler = MinMaxScaler()
        scaler.fit(train)
        train = scaler.transform(train)
        test = scaler.transform(test)

        n_input = 12
        n_features = 1

        generator = TimeseriesGenerator(train, train, length=n_input, batch_size=6)

        model = Sequential()
        model.add(LSTM(200, activation='relu', input_shape=(n_input, n_features)))
        model.add(Dropout(0.15))
        model.add(Dense(1))
        model.compile(optimizer='sgd', loss='mse')

        model.fit_generator(generator, epochs=300)

        pred_list = []

        batch = train[-n_input:].reshape((1, n_input, n_features))

        for i in range(n_input):
            pred_list.append(model.predict(batch)[0])
            batch = np.append(batch[:,1:,:], [[pred_list[i]]], axis=1)

        df_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index=df[-n_input:].index, columns=['Prediksi'])
        df_predict2 = scaler.inverse_transform(pred_list)
        df_test = pd.concat([df, df_predict], axis=1)

        df_test.tail(13)
        df_test.tail(13)

        plt.figure(figsize=(20, 5))
        plt.plot(df_test.index, df_test['data_content'])
        plt.plot(df_test.index, df_test['Prediksi'], color='r')
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        print(uri)
        context = {
            'matplot':uri,
            'title':'Training',
        }

        return render(request, 'home/hasil.html', context)

def testData(request):
        warnings.filterwarnings("ignore")
        queryset = str(datasCSV.objects.all().query)
        df = pd.read_sql_query(queryset, connection)
        df.nama_tahun = pd.to_datetime(df.nama_tahun)
        df = df.set_index('nama_tahun')
        print(df[['data_content']])

        df[['data_content']]
        df2 = df[['data_content']]
        df2

        train, test = df2[:-12], df2[-12:]
        train.tail(13)

        scaler = MinMaxScaler()
        scaler.fit(train)
        train = scaler.transform(train)
        test = scaler.transform(test)
        train3 = scaler.inverse_transform(train)
        train3

        n_input = 12
        n_features = 1

        generator = TimeseriesGenerator(train, train, length=n_input, batch_size=6)

        model = Sequential()
        model.add(LSTM(200, activation='relu', input_shape=(n_input, n_features)))
        model.add(Dropout(0.15))
        model.add(Dense(1))
        model.compile(optimizer='sgd', loss='mse')

        model.fit_generator(generator, epochs=180)
        model.summary()

        pred_list = []

        batch = train[-n_input:].reshape((1, n_input, n_features))

        for i in range(n_input):
            pred_list.append(model.predict(batch)[0])
            batch = np.append(batch[:,1:,:], [[pred_list[i]]], axis=1)

        df_predict = pd.DataFrame(scaler.inverse_transform(pred_list), index=df[-n_input:].index, columns=['Prediksi'])
        df_predict2 = scaler.inverse_transform(pred_list)
        df_test = pd.concat([df, df_predict], axis=1)
        pred_list
        df_predict2

        train = df2
        scaler.fit(train)
        train = scaler.transform(train)

        n_input = 12
        n_features = 1

        generator = TimeseriesGenerator(train, train, length=n_input, batch_size=6)
        model.fit_generator(generator, epochs=180)

        pred_list = []

        batch = train[-n_input:].reshape((1, n_input, n_features))

        for i in range(n_input):
            pred_list.append(model.predict(batch)[0])
            batch = np.append(batch[:,1:,:], [[pred_list[i]]], axis=1)

        from pandas.tseries.offsets import DateOffset
        add_dates = [df.index[-1] + DateOffset(months=x) for x in range(0,13) ]
        future_dates = pd.DataFrame(index=add_dates[1:],columns=df.columns)

        df_predict = pd.DataFrame(scaler.inverse_transform(pred_list),
                                index=future_dates[-n_input:].index, columns=['Predictions'])

        df_proj = pd.concat([df, df_predict], axis=1)


        df_proj.tail(14)

        plt.figure(figsize=(10,4))
        plt.plot(df_proj.index, df_proj['data_content'])
        plt.plot(df_proj.index, df_proj['Predictions'], color='r')
        plt.legend(loc='best', fontsize='large')
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        print(uri)
        context = {
            'matplot':uri,
            'title':'Testing',
        }

        return render(request, 'home/hasil.html', context)

        