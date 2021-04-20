from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('enterdata/',views.enterdata,name='enterdata'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout,name='logout'),

 
]
