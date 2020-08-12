from django.urls import path, include
from .views import index, LogoutView, dataUser, create, hasil
app_name ='home'
urlpatterns = [
    path('', index, name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('data/user', dataUser, name='datauser'),
    path('data/create', create , name='form'),
    path('data/hasil/', hasil, name='hasil')
]