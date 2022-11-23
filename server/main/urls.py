from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r"user", FetchViewsets, basename="github_user")

urlpatterns = router.urls
