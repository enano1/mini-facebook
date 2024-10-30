# In mini_fb/forms.py
from django import forms
from .models import Profile, StatusMessage


from django import forms
from django.contrib.auth.models import User
from .models import Profile, StatusMessage

# In mini_fb/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    # Fields for user authentication details
    username = forms.CharField(label="Username", max_length=150, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    
    # Additional profile fields
    fname = forms.CharField(label="First Name", max_length=100, required=True)
    lname = forms.CharField(label="Last Name", max_length=100, required=True)
    city = forms.CharField(label="City", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    image_url = forms.URLField(label="Profile Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['username', 'password', 'password_confirmation', 'fname', 'lname', 'city', 'email', 'image_url']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        
        # Check that both passwords match
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        # Create the User object with the provided username and password
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        
        # Link the Profile to the new User
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile

class CreateStatusMessageForm(forms.ModelForm):
    '''Form to post a new StatusMessage, with an option to upload an image.'''
    
    class Meta:
        model = StatusMessage
        fields = ['message']  

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']