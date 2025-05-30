from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


routers = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("chats.urls")),

    path('api/', include(routers.urls)),
    
    #enabling login and logout functionality for the API
    path('api-auth/', include('rest_framework.urls')),
]

