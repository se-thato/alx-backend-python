from django.urls import path
from . import views

urlpatterns = [
    path('delete-account/', views.delete_user, name='delete-account'),
     path('unread-messages/', views.unread_inbox, name='unread-messages'),
]
