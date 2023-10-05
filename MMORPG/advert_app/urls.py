from django.urls import path
from .views import (
    PostList, PostCreateView, PostDetail, CommentToPost, accept_comment, delete_comment
    )


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('comment/<int:pk>', CommentToPost.as_view(), name='write_comment'),
    path('accept/<int:id_comment>', accept_comment, name='accept_comment'),
    path('delete_comment/<int:id_comment>', delete_comment, name='delete_comment')
]

