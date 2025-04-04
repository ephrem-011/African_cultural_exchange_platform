from django.urls import path
from users import views
from django.contrib.auth.views import *

urlpatterns = [
    # path('', views.HomeView.as_view(), name = 'home'),
    path('signup/', views.SignUpView.as_view(), name= 'signup'),
    path('edit/<pk>', views.EditUserView.as_view(), name= 'edit_user'),
    path('dashboard/<int:pk>', views.dashboard.as_view(), name = 'dashboard'),
    path('login/', views.CustomLoginView.as_view(), name = 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_user/<int:userPK>', views.DeleteUser, name='delete_user'),
    path('register/', views.SignupAPI.as_view(), name='register'),
    path('deleteuser/<pk>', views.DeleteUser_.as_view(), name='deleteuser'),
    path('login_/', views.Login.as_view(), name='login_'),
    path('mydashboard/<pk>', views.MyDashboard.as_view(), name='mydashboard'),
    path('edituser/<pk>', views.EditUser_.as_view(), name='edituser'),
    path('logout_/', views.LogoutView.as_view(), name='logout_')
    

]