from django.urls import path
from . import views


app_name = 'api'


urlpatterns = [
    path('allowme/', views.openssh),
    path('checkme/', views.check_me),
    path('log/', views.log),
    path('domain/', views.domain),
    path('checkava/', views.checkAvailability),
    path('ddos/', views.ddos),

]
