from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.forms import UsersSignupForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer, NetworkEdgeCreationSerializer, NetworkEdgefollowerViewSerializer, NetworkEdgefollowingViewSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, NetworkEdge

# Create your views here.

def index(request):
    # print(f'Scheme: {request.scheme}')
    # print(f'Body: {request.body}')
    # print(f'Path: {request.path}')
    # print(f'Path Info: {request.path_info}')
    # # response_body = f'Scheme: {request.scheme} -- Body: {request.body} -- Path: {request.path} -- Path Info: {request.path_info} -- Query Param: {request'

    # response_body = f'My favourite colour: {request.GET["colour"]}'

    user_count = User.objects.count()
    users = User.objects.all()

    context = {
        'user_count':user_count,
        'users':users
    }

    return render(request, 'users/index.html', context)

# Currently serves both GET and POST requests
def signup(request):

    form = UsersSignupForm()
    # form = UserCreationForm()
    errors = []
    message = None

    if request.method == "POST":
        form = UsersSignupForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():            
            # Use commit = False to assign the object to the user. Using True will save the...
            # ...object in the db. After assignment we can do other things with the object.
            user = form.save(commit=False)
            user.save()
            message = 'Sign up successful'
            form = UsersSignupForm()
            # form = UserCreationForm()
        else:
            errors = form.errors
            form = UsersSignupForm(request.POST)
            # form = UserCreationForm(request.POST)

    context = {
        'form':form,
        'errors':errors,
        'message':message
    }

    return render(request, 'users/signup.html', context)

@api_view(['POST'])
def create_user(request):
    
    # Converting python objects -> native data types -> into json/xml => Representing data

    # {
    #     "first_name":"Varun",
    #     "last_name":"Jain",
    #     "email":"varun@scaler.com"
    # }

    # user = User()

    # user.first_name = request.data['first_name']
    # user.last_name = request.data['last_name']
    # user.email = request.email['email']

    # user.save()
    
    # Problems with this approach

    # Maintenance
    # Every time we make change to the model we will have to change code which is inconvenient.

    # Stability
    # Complex web applications will have large number of attributes. It will be cumbersome to map 
    # each attribute from json to the object attributes.

    # Deserialization - json_input -> native_data_types -> orm_objects -> db_row => Creating data

    # Serializers/Deserializers couple the model attributes and the json inputs and maps it automatically.

    serializer = UserCreateSerializer(data=request.data)

    response_data = {
        "errors":None,
        "data":None
    }

    # Authentication vs Authorization

    # Set authentication scheme in setting.py in a dictionary

    # REST_FRAMEWORK = {
    #     'DEFAULT_AUTHENTICATION_CLASSES': [
    #         'rest_framework.authentication.BasicAuthentication',
    #         'rest_framework.authentication.SessionAuthentication',
    #     ]
    # }

    # Here we are telling django to authenticate incoming requests using the code in the path
    # provided.

    # The other way is to use decorators. 
    # 
    # @api_view(['GET'])
    # @authentication_classes([SessionAuthentication, BasicAuthentication])
    # @permission_classes([IsAuthenticated])
    # def example_view(request, format=None):
    #     content = {
    #       'user':str(request.user),
    #       'auth':str(request.auth),
    #       }         
    #     return Response(content)
    #
    # One of the advantages of using decorators is that we
    # can pick and choose where to apply authentication procedures. 
    #
    # Once we authenticate, request.user and request.auth attributes are set. 


    # First one is a global setting while the second one is a local setting. 
    # 
    # Types of authentication schemes

    # 1. Basic Authentication. request.user will be set to Django user instance and request.auth
    # will be set to None.

    # 2. Token Authentication. This is appropriate for client-server setups, such as native
    # desktop and mobile clients. Tokens are alphanumeric strings that are sent and store in the
    # clients side. Every request from the clients side carries this token. 
    # There are third party libraries that do this as well. Oauth, JSON Web Token (JWT)

    # JWT
    # We could add this in the REST_FRAMEWORK dictionary. 
    #
    # After sign up, we want to log the user in. So we send a token in the response to the 
    # POST request. The client can then use the token to access the other functionalities of 
    # the website. We can manually generate such a token.
    #
    # JWT refresh token and access token has a time limit. By default refresh token lasts for a day
    # and access token lasts for 5 mins. When access token expires, the client uses the refresh
    # token to generate a new access token.

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data['data'] = {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        response_status = status.HTTP_201_CREATED
    else:
        response_data['errors'] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

 
    return Response(response_data, status=response_status)

# This is the view method that we use to get a list of users. Only users who have logged in
# should be able to see a list of all users. So a user have to use the access token generated in the
# login method to access the user list.

# The response of the profile view should also include some attributes of the user model as well.

# Change this to a class based view. This class will, highly likely, have only the get method.  
# Implement this using a list mixin.
@api_view(['GET'])
@authentication_classes([JWTAuthentication]) # Here we are setting the authentication class as JWTAuthentication.
@permission_classes([IsAuthenticated])
def user_list(request):
    
    users = UserProfile.objects.all()

    # We can get the user who made this request if the user sends an authorization header with 
    # value as Bearer <access_token>
    # This object is important when we want to log who liked a particular post.
    print(request.user)
    # When we get POST data, we pass it to the serializer as the data argument. When we 
    # send data as response, we pass the object as the instance argument.
    serialized_data = UserProfileViewSerializer(instance=users, many=True)
    # response_data = {
    #     "errors":None,
    #     "data":None
    # }

    # serialized_data.data contains a dictionary which is converted to JSON by Response
    return Response(serialized_data.data, status=status.HTTP_200_OK)


class UserProfileDetail(APIView):

    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    # TODO: Approach1: Update this endpoint to respond with a users post along with the profile.
    # TODO: Approach2: Setup another endpoint in the content view, to get the posts of a user.

    def get(self, request, pk):
        user = UserProfile.objects.filter(id=pk).first()
        if user:
            serializer = UserProfileViewSerializer(instance=user)
            response_data = {
                "data":serializer.data,
                "error":None
            }
            response_status = status.HTTP_200_OK
        else:
            response_data = {
                "data":None,
                "error":"User does not exist"
            }
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response_data, status=response_status)

    def post(self, request, pk):
        
        user_profile_serializer = UserProfileUpdateSerializer(
                                instance=request.user.profile,
                                data=request.data)
        response_data = {
            'data':None,
            'errors':None
        }

        # If the data is valid, save the modification in the db. 
        if user_profile_serializer.is_valid():
            user_profile = user_profile_serializer.save()
            response_data['data'] = user_profile_serializer.data
            response_status = status.HTTP_202_ACCEPTED
        else:
            response_data['errors'] = user_profile_serializer.errors
            response_status = status.HTTP_404_NOT_FOUND
        
        return Response(response_data, status=response_status)

    def delete(self, request, pk):
        user = request.user
        user.delete()
        response_data = {
            "data":None,
            "message":"User object deleted successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Class based views is that it allows us to easily compose reusable bits of behviour.

# There are mixins for listing, creating, retreiveing, updating and destroying models. 

# These mixins are basically generalising boilerplate code so that our functions and classes
# are neat and crisp.

# GenericAPIView has methods like get_queryset(), get_object(), get_serializer(),
# get_serializer_class(), get_serializer_context(), filter_queryset()

# get_queryset() accesses the queryset variable and executes it.
# get_serializer_class() gets the serializer class that has been defined. 
# These methods have default behaviour or we could also overwrite the behaviour of the mixins.
# 
# We override the default behaviour when we want to include our own business logic.  
class UserNetworkEdgeView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        generics.GenericAPIView):
    
    # Queryset is something that generics expects
    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    #We need the NetworkEdgeViewSerializer class for the get request
    def get_serializer_class(self):
        # TODO: Change the serializer in case followers are being requested
        if self.request.method != 'GET':
            return super().get_serializer_class()

        edge_direction = self.request.query_params['direction']
        if edge_direction == 'followers':
            return NetworkEdgefollowerViewSerializer
        elif edge_direction == 'following':
            return NetworkEdgefollowingViewSerializer
    
    
    def get_queryset(self):

        edge_direction = self.request.query_params['direction']
        if edge_direction == 'followers':
            # NetworkEdge.objects.all().filter()
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == 'following':
            return self.queryset.filter(from_user=self.request.user.profile)
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # The create method just takes the request data and passes it to the serializer class
        # Then it calls perform create with the serializer instance and returns a response object. 

        # When we call the API to create a network edge, the user calling the API is the from_user
        # and we have to include the to_user in the request body.

        # TODO: Using the serializer context object

        request.data['from_user'] = request.user.profile.id

        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        #TODO: Implement this using the network edge pk and destroy mixin.

        network_edge = NetworkEdge.objects.filter(
                                        from_user=request.user.profile,
                                        to_user = request.data['to_user']    
                                        )
        if network_edge.exists():
            network_edge.delete()
            message = 'Unfollowed user'
        else:
            message = 'Relationship does not exist'
        
        return Response({'data':None, 'message':message}, status=status.HTTP_202_ACCEPTED)
