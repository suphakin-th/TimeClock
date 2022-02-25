from django.conf.urls import url
from django.urls import include
from django.urls.conf import path
from rest_framework.routers import DefaultRouter, Route

from time_clock import settings
from .views_is_authenticated import IsAuthenticatedView
from .views_login import LoginView
from .views_logout import LogoutView
from .views_profile import ProfileView
from .views_register import RegisterView
from .views_clocking import ClockingView

router = DefaultRouter()
router.include_root_view = settings.ROUTER_INCLUDE_ROOT_VIEW
router.routes[0] = Route(
    url=r'^{prefix}{trailing_slash}$',
    mapping={
        'get': 'list',
        'post': 'create',
        'patch': 'profile_patch',
    },
    name='{basename}-list',
    detail=False,
    initkwargs={'suffix': 'List'}
)
router.register(r'login', LoginView)
router.register(r'clock', ClockingView)
router.register(r'profile', ProfileView)
router.register(r'register', RegisterView)


urlpatterns = [
    url(r'is-authenticated/$', IsAuthenticatedView.as_view()),
    url(r'logout/$', LogoutView.as_view()),

    url(r'^', include(router.urls)),
]
