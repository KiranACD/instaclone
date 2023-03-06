
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile, NetworkEdge

class UserCreateSerializer(ModelSerializer):

    # Override the method in the modelserializer when we want to do custom procedures.
    # For example, before saving the password we need to hash the password.
    # Important to run the is_valid() method before calling this function. Because validated_data
    # is set only after is_valid() method is called. 
    def create(self, validate_data):
        validate_data['password'] = make_password(validate_data['password'])

        # kwargs here makes the app extensible
        user = User.objects.create(**validate_data)
        UserProfile.objects.create(user=user)
        # It is important to return the user instance or else serializer.save() will not 
        # return the user instance
        return user

    class Meta:
        model = User

        # fields, include, exclude
        # Will map these values on either side.
        fields = ('username', 'password', 'email', )

# We dont want to send password or email back to the frontend.
# However, we cannot remove the password or email from the UserCreateSerializer because then
# the create_user will stop working.
# So, we create a UserViewSerializer.
class UserViewSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', )

class UserProfileViewSerializer(ModelSerializer):

    user = UserViewSerializer()

    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic_url', 'user', )

        # exclude = ('id', 'is_verified',) # This is a blacklist

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',)
        # fields = ('first_name', 'last_name', 'username', )
    
    def update(self, instance, validated_data):
        print('instance: ', instance)
        print('UserUpdateValidatedData: ', validated_data)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.username = validated_data.get('username', instance.username)
        return instance
    

class UserProfileUpdateSerializer(ModelSerializer):

    user = UserUpdateSerializer()

    class Meta:
        model = UserProfile
        fields = ('bio','profile_pic_url','user',)
        # fields = ('bio', 'profile_pic_url',)
    
    def validate_user(self, user_data):

        user_update_serializer = UserUpdateSerializer(instance = self.instance.user, data=user_data)
        if user_update_serializer.is_valid():
            # print(user)
            user_update_serializer.save()
            return user_data
        raise ValidationError({'user':'Please enter first name'})

    def update(self, instance, validated_data):
        print('Validated Data: ', validated_data)
        # user_update_serializer = self.fields['user']
        # user_data = validated_data.get('user')
        # user = User.objects.get(id=user_data.id)
        return instance

class NetworkEdgeCreationSerializer(ModelSerializer):

    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user',)

class NetworkUserProfileViewSerializer(ModelSerializer):

    user = UserViewSerializer()
    follower_count = SerializerMethodField()
    following_count = SerializerMethodField()
    
    # TODO: Include the id in the user information as well, So that the frontend can use them.

    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic_url', 'user', 'follower_count', 'following_count')
    
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()


class NetworkEdgefollowerViewSerializer(ModelSerializer):

    from_user = NetworkUserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('from_user', )

class NetworkEdgefollowingViewSerializer(ModelSerializer):

    to_user = NetworkUserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('to_user', )

