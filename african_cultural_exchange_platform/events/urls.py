from django.urls import path
from events import views

urlpatterns = [
    path('addevent/', views.CreateEvent.as_view(), name= 'addevent'),
]