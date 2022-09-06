from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostDeleteViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts-delete', PostDeleteViewSet, basename='posts-delete')

urlpatterns = [
    path('', include(router.urls)),
]
