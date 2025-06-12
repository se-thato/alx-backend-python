from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


routers = DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("chats.urls")),
    path('', include("messaging.urls")),

    path('api/', include(routers.urls)),
    
    #enabling login and logout functionality for the API
    path('api-auth/', include('rest_framework.urls')),

     # JWT authentication endpoints
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

     #Session login/logout 
    path('api/auth/', include('rest_framework.urls')),
]

