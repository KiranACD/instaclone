from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UsersSignupForm(UserCreationForm):
    
    # first_name = forms.CharField(
    #                 required=True,
    #                 widget=forms.widgets.TextInput(
    #                     attrs={
    #                         "placeholder":"Enter your first name",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="First Name")
    
    # last_name = forms.CharField(
    #                 required=True,
    #                 widget=forms.widgets.TextInput(
    #                     attrs={
    #                         "placeholder":"Enter your last name",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="Last Name")

    # email = forms.EmailField(
    #                 required=True,
    #                 widget=forms.widgets.TextInput(
    #                     attrs={
    #                         "placeholder":"Enter your email address",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="Email")
    
    # phone_number = forms.CharField(
    #                 required=True,
    #                 widget=forms.widgets.TextInput(
    #                     attrs={
    #                         "placeholder":"Enter your phone number",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="Phone Number")

    # user_name = forms.CharField(
    #                 required=True,
    #                 widget=forms.widgets.TextInput(
    #                     attrs={
    #                         "placeholder":"Enter your username",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="Username")

    # password = forms.CharField(
    #                 required=True,
    #                 widget=forms.widgets.PasswordInput(
    #                     attrs={
    #                         "placeholder":"Enter your password",
    #                         "class":"input-fields"
    #                     }
    #                 ), label="Password")
    

    class Meta:
        model = User
        # exclude = ('phone_number',)
        fields = ('username', 'first_name', 'last_name', 'email', 'password1')
        
        # exclude = ('created_on', 'updated_on', 'is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login')


