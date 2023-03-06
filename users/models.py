from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):

#     name = models.CharField(max_length=255, null=False)
#     email = models.EmailField(max_length=255, unique=True, null=False)
#     password = models.CharField(max_length=55, null=False)
#     phone_number = models.CharField(max_length=10, unique=True)
#     is_active = models.BooleanField(default=False)

#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

class TimeStamp(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class UserProfile(TimeStamp):

    # ToDo: ADD Verification for size and type of profile pic. Change profile pic to ImageField.
    # ToDo: Modify the naming of the file being saved so that the update view becomes idempotent
    # or compliant with put request.
    #  
    DEFAULT_PROFILE_PIC_URL = "https://mywebsite.com/placeholder.png"
    
    # One user can have only one profile
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=False)
    profile_pic_url = models.CharField(max_length=255, default=DEFAULT_PROFILE_PIC_URL)
    bio = models.CharField(max_length=255, blank=True)

    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_verified = models.BooleanField(default=True)

# Network - edges

# A --------> B
# B --------> A

# user_a => Who does user_a follow?
# NetworkEdge.objects.filter(from_user=user_a)
# user_a.following.all() -> [B, C]  -> Two Edges
# user_a.followers

# user_b

# TODO: Create a system for private profiles where users can decide who follows them.

class NetworkEdge(TimeStamp):
    from_user = models.ForeignKey(
                UserProfile,
                on_delete=models.CASCADE,
                related_name='following'
    )
    to_user = models.ForeignKey(
                UserProfile,
                on_delete=models.CASCADE,
                related_name='followers'
    )
    class Meta:
        unique_together = ('from_user', 'to_user', )