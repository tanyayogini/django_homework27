from django.urls import path
from rest_framework import routers

from ads.views import AdViewSet, AdImageView

router = routers.SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
    path('<int:pk>/upload_image/', AdImageView.as_view()),

]

urlpatterns += router.urls
