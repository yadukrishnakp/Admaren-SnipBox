from django.urls import path
from . import views


urlpatterns = [

    path('login', views.LoginApiView.as_view()),
    path('refresh-token', views.RefreshTokenView.as_view()),
]