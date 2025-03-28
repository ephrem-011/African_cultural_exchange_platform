from django.urls import path
from events import views

urlpatterns = [
    path('addevent/', views.CreateEvent.as_view(), name= 'addevent'),
    path('eventlist', views.EventList.as_view(), name='eventlist'),
    path('joinevent/<pk>', views.JoinEvent.as_view(), name='joinevent'),
    path('myevents/<pk>', views.MyEvents.as_view(), name='myevents'),
    path('update_event/<pk>', views.UpdateEvent.as_view(), name='update_event'),
    path('view_event/<pk>', views.ViewEvent.as_view(), name='view_event'),
    path('leave_event/<int:event>/', views.LeaveEvent, name='leave_event'),
    path('view_attendees/<pk>', views.ViewAttendees.as_view(), name='view_attendees'),
    path('delete_event/<int:eventPK>', views.DeleteEvent, name='delete_event'),
    
]