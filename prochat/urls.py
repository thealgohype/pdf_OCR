from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ravidata_new', views.ravinew, name='ravi_baba_new')
]
