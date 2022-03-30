from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaign import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'campaign'

urlpatterns = [
    path('', include(router.urls))
]
