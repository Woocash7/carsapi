from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet, basename='car')

app_name = 'api'

urlpatterns = router.urls
urlpatterns += [
    path('rate/', views.RateCreate.as_view(), name='rate-detail'),
    path('popular/', views.PopularCarList.as_view(), name='popular-list')
]