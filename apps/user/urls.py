from . import views
from django.urls import path

urlpatterns = [
    path('create-or-update-user', views.CreateOrUpdateUserApiView.as_view()),
    path('get-users-list', views.GetUsersListApiView.as_view()),
    path('get-user-details', views.GetUserDetailApiView.as_view()),
]