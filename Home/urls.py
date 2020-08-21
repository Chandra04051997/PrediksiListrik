from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index,
    LogoutView, 
    dataUser, 
    create, 
    hasil, 
    uploadCSV, 
    CSVListView, 
    deleteAll,
    testData,
    trainData
)
app_name ='home'
urlpatterns = [
    path('', index, name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('data/user', dataUser, name='datauser'),
    path('data/create', create , name='form'),
    path('data/hasil/', hasil, name='hasil'),
    path('data/csv/', uploadCSV, name='csv'),
    path('data/csv/list' , CSVListView.as_view(), name='csvlist'),
    path('data/csv/delete/all', deleteAll, name='deleteAll'),
    path('data/train/', trainData, name='train'),
    path('data/test/', testData, name='test')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)