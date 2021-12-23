from django.urls import path
from . import views

# Super User - Rahul_Roy_21, Rahul1234
app_name = "chat"

urlpatterns = [
	path('', views.home, name="home"),
	path('login', views.loginuser, name="login"),
	path('logout', views.logoutuser, name="logout"),
	path('register', views.register, name="register"),
	
	path('checkoutroom/<str:room>/', views.checkoutroom, name='checkoutroom'),
    path('checkroom', views.checkroom, name='checkroom'),
	path('createroom', views.createroom, name='createroom'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]


# urlpatterns = [
#     path('', views.home, name='home'),
#     path('<str:room>/', views.room, name='room'),
#     path('checkview', views.checkview, name='checkview'),
#     path('send', views.send, name='send'),
#     path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
# ]