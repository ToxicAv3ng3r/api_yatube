from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from .views import PostListViewSet, GroupListViewSet, CommentListViewSet

router = SimpleRouter()
router.register(r'posts', PostListViewSet)
router.register(r'groups', GroupListViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentListViewSet,
    basename='comment'
)


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
]
