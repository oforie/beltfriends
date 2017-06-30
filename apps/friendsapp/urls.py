from django.conf.urls import url
from . import views 

app_name='friends'  

urlpatterns = [
    url(r'^', views.index, name='index'),
    url(r'^(?P<id>/d+)$', views.others, name='others'),
    url(r'^newfriend$', views.addtoFriends, name='newfriend'),
]