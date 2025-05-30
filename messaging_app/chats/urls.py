from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet



router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Nested router for messages under conversations
conversations_router = router.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(conversations_router.urls)), 
]


