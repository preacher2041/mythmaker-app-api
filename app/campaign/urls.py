from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaign import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('world', views.WorldViewSet)

app_name = 'campaign'

urlpatterns = [
    path('', include(router.urls))
]
