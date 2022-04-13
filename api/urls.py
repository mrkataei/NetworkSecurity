from . import views
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('allowme/', openssh),
    path('checkme/', checkme),
    path('log/', log),
    path('checkava/', checkAvailability),
    path('ddos/', ddos),
    path('domain/', domin)
]
