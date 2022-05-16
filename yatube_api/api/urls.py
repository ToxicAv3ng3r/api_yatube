from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from .views import PostListViewSet, GroupListViewSet, CommentListViewSet

router = SimpleRouter()
router.register(
    'v1/posts',
    PostListViewSet,
    basename='post'
)
router.register(
    'v1/groups',
    GroupListViewSet,
    basename='group'
)
router.register(
    r'v1/posts/(?P<post_id>\d+)/comments',
    CommentListViewSet,
    basename='comment'
)


urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
]
