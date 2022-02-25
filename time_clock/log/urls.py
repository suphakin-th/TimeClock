from rest_framework import routers

from .views import LogDeviceView

router = routers.DefaultRouter()
router.register(r'log_device', LogDeviceView)

app_name = 'log'
urlpatterns = router.urls
