from django.urls import path
from events import views

urlpatterns = [
    path('addevent/', views.CreateEvent.as_view(), name= 'addevent'),
    path('eventlist', views.EventList.as_view(), name='eventlist'),
    path('joinevent/<pk>', views.JoinEvent.as_view(), name='joinevent'),
    
]