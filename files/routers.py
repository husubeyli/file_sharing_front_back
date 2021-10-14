from rest_framework.routers import DefaultRouter

from .viewsets import CommentViewsets


router = DefaultRouter()
router.register(r'comments', CommentViewsets, basename='comments')