from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaign import views


router = DefaultRouter()
router.register('campaigns', views.CampaignViewSet)
router.register('tags', views.TagViewSet)
router.register('worlds', views.WorldViewSet)

app_name = 'campaign'

urlpatterns = [
    path('', include(router.urls))
]
