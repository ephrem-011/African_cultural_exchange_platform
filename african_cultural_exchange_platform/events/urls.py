from django.urls import path
from events import views

urlpatterns = [
    path('addevent/', views.CreateEvent.as_view(), name= 'addevent'),
    path('eventlist', views.EventList.as_view(), name='eventlist'),
    path('joinevent/<pk>', views.JoinEvent.as_view(), name='joinevent'),
    path('myevents/<pk>', views.MyEvents.as_view(), name='myevents'),
    path('update_event/<pk>', views.UpdateEvent.as_view(), name='update_event'),
    path('view_event/<pk>', views.ViewEvent.as_view(), name='view_event'),
    
]