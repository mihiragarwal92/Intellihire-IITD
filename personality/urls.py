from django.urls import path
from personality import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "personality"

urlpatterns = [

    path('index/predict', views.home, name='index'),
    path('index/submit', views.result, name='result'),
 
]
