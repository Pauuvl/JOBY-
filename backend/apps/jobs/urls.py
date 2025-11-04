from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, SavedJobViewSet

router = DefaultRouter()
router.register(r'', JobViewSet, basename='job')
router.register(r'saved', SavedJobViewSet, basename='saved-job')

urlpatterns = [
    path('', include(router.urls)),
]
