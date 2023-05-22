from rest_framework import routers

from ads.views import SelectionViewSet

router = routers.SimpleRouter()
router.register('', SelectionViewSet)
urlpatterns = router.urls
