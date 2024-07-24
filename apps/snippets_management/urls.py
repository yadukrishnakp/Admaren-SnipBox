from django.urls import path
from apps.snippets_management import views

urlpatterns = [
    path('get-count-and-details-list', views.GetSnippetsCountAndDeatilsListApiView.as_view()),
    path('create-snippets', views.CreateSnippetsApiView.as_view()),
    path('get-snippet-details-current-user', views.GetSnippetsDeatilsCurrentUserApiView.as_view()),
    path('update-snippets', views.UpdateSnippetsApiView.as_view()),
    path('delete-snippets', views.DeleteSnippetsApiView.as_view()),
    path('get-tag-list', views.GetTagListApiView.as_view()),
    path('get-tag-detailed', views.GetTagDetailedApiView.as_view()),
]