from django.urls import path

from loginapp import views

urlpatterns = [
    path('login/',views.login),
    path('saveUser/',views.saveUser),
    path('givemepage1',views.giveMePage1),
 
]

