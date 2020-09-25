from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # adv/23/
    #path('<int:album_id>/', views.details, name='details'),
    # url('^(?P<album_id>[0-9]{4})/$',views.details,name='details')
    #path('adv/',views.adv,name='adv'),
]