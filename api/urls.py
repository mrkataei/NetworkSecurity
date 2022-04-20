from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'api'

router = DefaultRouter()
router.register('log', views.LogViewSet)

urlpatterns = [
    path('allowme/', views.openssh),
    path('checkme/', views.check_me),
    path('domain/', views.domain),
    path('checkava/', views.checkAvailability),
    path('ddos/', views.ddos),
    path('post-ip/', views.post_white_ip),
    path('get-ip/', views.get_white_ips),
    path('get-update-delete-ip/<pk>', views.get_update_delete_white_ip),
    path('search-ip', views.search_ip)
]

urlpatterns += router.urls
