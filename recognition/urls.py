from django.urls import path
from recognition import views
app_name = "recognition"
urlpatterns = [

    path('index/question', views.questions, name='questionPage')

 
]
