from django.urls import path
from . import views

urlpatterns = [
    path("",views.PostList.as_view(),name="postlist"),
    path("<int:pk>/",views.PostDetail.as_view(),name="detail"),
    path("<int:pk>/comment/",views.CommentList.as_view(),name="comment"),
    path("comment/<int:comment_pk>/",views.CommentDetail.as_view(),name="comment_detail"),
    path("<int:pk>/like/",views.LikeList.as_view(),name="like"),
]
