from django.db import models
from users.models import TimeStamp, UserProfile

# Create your models here.

# We want the user to be able to upload n number of photos or videos in a post.

class UserPost(TimeStamp):

    caption_text = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')
    is_published = models.BooleanField(default=False)

class PostMedia(TimeStamp):

    def media_name(instance, file_name):
        ext = file_name.split('.')[-1]
        # TODO: Implment uuid instead of post id.
        return f'{instance.post.id}_{instance.sequence_index}.{ext}'

    # Using file field here, because this needs to contain both images and videos
    # We have to accept files of a certain type and size. 
    media_file = models.FileField(upload_to=media_name)
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='media')

    class Meta:
        # One post should have unique media sequence number
        unique_together = ('sequence_index', 'post',)
    
# TODO: Implement reactions instead of likes.
class PostLikes(TimeStamp):

    #post.likes.all()
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='likes')
    #user.liked_post.all()
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        unique_together = ('post', 'liked_by')

# TODO: Implement Nested Comments
# TODO: Implement likes Comments
class PostComments(TimeStamp):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments_made')
    text = models.CharField(max_length=255)