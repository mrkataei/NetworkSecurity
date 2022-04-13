from . import views
from django.urls import path
from . import views
app_name = 'api'
urlpatterns = [
    path('allowme/', views.openssh),
    path('checkme/', views.check_me),
    # path('log/', log),
    # path('checkava/', checkAvailability),
    # path('ddos/', ddos),
    # path('domain/', domin)
]
