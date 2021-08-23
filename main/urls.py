from django.urls import path ,include
from .views import *

urlpatterns = [
    path('allowme/' , openssh),
    path('checkme/' , checkme),
    path('log/', log),
    path('checkava/',checkAvailability),
    path('ddos/',ddos),
    path('domain/',domin)
]
