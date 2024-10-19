# In mini_fb/forms.py
from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fname', 'lname', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''Form to post a new StatusMessage, with an option to upload an image.'''
    
    image_file = forms.ImageField(required=False)  # Optional field for image upload
    
    class Meta:
        model = StatusMessage
        fields = ['message']  # Keep only the message field for the status
