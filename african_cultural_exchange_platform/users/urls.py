from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name= 'signup'),
    path('edit/<pk>', views.EditUserView.as_view(), name= 'edit_user'),
    path('dashboard/<pk>', views.dashboard.as_view(), name = 'dashboard'),
]