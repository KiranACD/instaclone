from django.shortcuts import render

# Create your views here.

from .models import UserPost, PostLikes, PostComments
from .serializers import UserCreatePostSerializer, PostMediaCreateSerializer, PostFeedSerializer, PostLikeCreateSerializer
from .filters import CurrentUserFollowingFilterBackend
from rest_framework import generics, mixins, viewsets, response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserPostCreateFeed(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = UserPost.objects.all()
    serializer_class = UserCreatePostSerializer
    filter_backends = [CurrentUserFollowingFilterBackend, ]

    # TODO: Create a System to follow topics or hashtags
    # TODO: Create a way of ordering the feed - eg. post popularity

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {'current_user':self.request.user.profile}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# Create post with user id.
# upload media files with the reference post id obtained from step 1.
# update the post and publish.

class PostMediaView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = PostMediaCreateSerializer
    

    # Put request here to make the request idempotent. We want the frontend to have the 
    # ability to perform a retry to upload content files. 
    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserPostDetailUpdateView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserCreatePostSerializer
    queryset = UserPost.objects.all()

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return PostFeedSerializer
        return self.serializer_class

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    # TODO: Filter posts that are not published yet.
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # TODO: Create an endpoint to delete a post


# ViewSets standardizes URL construction. It becomes compliant with REST principles. It gives a
# a lot of functionality out of the box. 

# viewsets.ViewSet
# URLs get configured immediately, however, the methods need to implemented for the verbs to work.
# Implment list , create, retreive etc.

# viewsets.GenericViewSet
# GENERICViewset - Similar to viewset. We can add mixins. Then the methods become automatically
# available. We can add mixins only with generic viewset. Mixins need a serializer class. 
# We can also override get_queryset or get_serializer_class etc.

# viewsets.ModelViewSet
# ModelViewSet - urls and methods are included. We dont need to use anything. When we know that
# the resource will be handled in a standard way, then we can use ModelViewSet. We can disable
# certain methods in the model viewset if we want.

class PostLikeViewSet(mixins.CreateModelMixin,
            mixins.ListModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeCreateSerializer

    def get_serializer_context(self):
        return {'current_user':self.request.user.profile}

    # We are defining this method to list likes by post
    def list(self, request):
        
        # TODO: Implement a serializer for the like list. We want the user profile to show up
        # in the like list
        
        # We are not using a filter backend here, because filter backend is applied on every
        # get.object method. It will affect delete mixins as well.
        post_likes = self.queryset.filter(post_id=request.query_params['post_id'])
        page = self.paginate_queryset(post_likes)

        # This is to handle multiple pages
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_likes, many=True)
        return response.Response(serializer.data)

