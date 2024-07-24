from django.urls import path
from apps.snippets_management import views

urlpatterns = [
    path('get-count-and-details-list', views.GetSnippetsCountAndDeatilsListApiView.as_view()),
    path('create-snippets', views.CreateSnippetsApiView.as_view()),
    path('update-snippets', views.UpdateSnippetsApiView.as_view()),
]