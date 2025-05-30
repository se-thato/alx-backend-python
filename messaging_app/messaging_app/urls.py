from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


routers = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("chats.urls")),

    path('api/', include(routers.urls)),
]

