from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Article
from .bnn import bnn

# Create your views here.
@login_required
def index(request):
    artikel = Article.objects.all()
    user = User.objects.all()
    context={
        'title':'Home',
        'dataUser':user,
        'dataArtikel':artikel,
        'pageTitle':'Dashboard',
        # 'prediksi':bnn()
        'active':'active'
    }
    return render(request, 'index.html', context)

def dataUser(request):
    context={
        'pageTitle':'Data User',
        'active':'active'
    }
    return render(request, 'home/userlist.html', context)

class LogoutView(RedirectView):

    url = '/admin/login/?next=/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)