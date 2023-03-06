from rest_framework.serializers import ModelSerializer
from .models import UserPost, PostMedia, PostLikes, PostComments
from users.serializers import NetworkUserProfileViewSerializer

class UserCreatePostSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']
        print(validated_data)
        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ('caption_text', 'location', 'id', 'is_published', )

class PostMediaCreateSerializer(ModelSerializer):
    
    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post', )

class PostMediaViewSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        exclude = ('post', )

# We need a postFeedSerializer instead of UserCreatePostSerializer because we will need to carry
# a lot more information in the posts that appear in the feed.
class PostFeedSerializer(ModelSerializer):

    # TODO: Create an appropriate serializer for this user profile view in a feed purpose.
    author = NetworkUserProfileViewSerializer()
    # This is a one-to-many relattionship, so we have to specify many=True
    media = PostMediaViewSerializer(many=True)

    class Meta:
        model = UserPost
        fields = '__all__'
        # This will include all the fields apart from those in the fields tuple
        include = ('media', )


class PostLikeCreateSerializer(ModelSerializer):

    # Because we dont want to get the user id from the frontend.
    def create(self, validated_data):
        validated_data['liked_by'] = self.context['current_user']
        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('id', 'post', )