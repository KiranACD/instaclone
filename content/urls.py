from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like', views.PostLikeViewSet)
# GET but no param - List
# GET with path param - Retreive
# POST - create
# PUT - needs path param to work - update
# PATCH - needs path param to work - partial_update
# DELETE - needs path param to work - delete


# Create a post
# Upload media
# View post - feed, postdetail

# Every image/video is uploaded individually using the upload media endpoints. 
# The post is created with no media/caption because it is needed as reference. This is because
# when inserting the media we need the post id too.

# Once the user post is created, it will be returned to the frontend app. Then post requests
# are made to the media endpoints. Once the media has been uploaded, the user will add location,
# caption etc. Once this is done, we can toggle is_published to True. 

# All of the changes that we make to the post object is made using the update endpoint. 

urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name='user_post_view'),
    path('media/', views.PostMediaView.as_view(), name='post_media_view'),  
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name='user_post_detail_update_view')

]