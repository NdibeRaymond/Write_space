from django.urls import path
from . import views

app_name = "posts_api"

urlpatterns = [

 # path("<str:username>/post/all/",views.userPostListView.as_view(),name="user_post_list"),
 # path('<str:username>/post/<int:pk>/',views.userPostDetailView.as_view(),name="user_post_detail"),
 # path("<int:pk>/unsave/",views.postUnsaveView.as_view(),name="unsave"),
 # path('<int:pk>/save_for_future/',views.postSaveView.as_view(),name="save_for_future"),
 path("all/",views.postListApiView.as_view(),name="post_list"),
 path('<int:pk>/',views.postDetailApiView.as_view(),name="post_detail"),
 path("<str:username>/new/",views.postCreateApiView.as_view(),name="create_post"),
 path('<int:pk>/edit/',views.postUpdateApiView.as_view(),name="edit_post"),
 path('<str:username>/<int:pk>/delete/',views.postDeleteApiView.as_view(),name="delete_post"),
 path('<int:pk>/comments/',views.commentsApiView.as_view(),name="comments"),
 path('<int:pk>/comments/add/',views.addCommentApiView.as_view(),name="add_comment"),
 path('comments/<int:pk>/edit/',views.editCommentApiView.as_view(),name="edit_comment"),
 # path("<str:username>/saved/",views.savedListView.as_view(),name="view_saved"),
 # path('<int:pk>/comment/',views.add_comment_to_post,name="add_comment_to_post"),
 # path('<int:pk>/clap/',views.postClapView.as_view(),name="clap"),
 # path('cartegory/<str:name>/',views.cartegoryView.as_view(),name="cartegory"),
 # path('<int:pk>/publish/',views.post_publish,name="post_publish"),
 # path('<int:pk>/unpublish/',views.post_unpublish,name="post_unpublish"),
 # path('join_cartegory/<int:pk>/',views.join_cartegory_view,name="join_cartegory"),
 # path('leave_cartegory/<int:pk>/',views.leave_cartegory_view,name="leave_cartegory"),

]
