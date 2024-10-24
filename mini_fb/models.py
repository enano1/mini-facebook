from django.db import models
from django.urls import reverse
# from typing import Any

# Create your models here.
class Profile(models.Model):
    '''
    Encapsulate the idea of one Profile by some user.
    '''

    fname = models.TextField(blank=False) #cannot be blank
    lname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=False) #optional field


    def __str__(self):
        '''
        Return a string representation of this object.
        '''

        return f'''{self.fname} {self.lname}'''
    
    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    
    def get_friends(self):
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)
        return friend_profiles

    def add_friend(self, other):
        """Add another profile as a friend if no duplicate relationship exists."""
        if self == other:
            # Prevent self-friending
            return

        # Check if the friend relationship already exists
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        if not existing_friendship:
            # If no existing friendship, create one
            Friend.objects.create(profile1=self, profile2=other)

    def get_friends(self):
        """Retrieve all friends of this profile."""
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)
        return friend_profiles

    def get_friend_suggestions(self):
        """Get friend suggestions for this profile."""
        # Get all profiles except the current one and current friends
        friends = self.get_friends()
        all_profiles = Profile.objects.exclude(pk=self.pk)
        suggested_friends = all_profiles.exclude(pk__in=[friend.pk for friend in friends])
        return suggested_friends


    def get_absolute_url(self):
        return reverse('show_profile', args=[str(self.pk)])
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.timestamp} - {self.message[:20]}..."
    
    def get_images(self):
        '''Return all images associated with this StatusMessage.'''
        return self.images.all()  
    
class Image(models.Model):
    '''
    Encapsulate the idea of an image attached to a StatusMessage.
    '''
    image_file = models.ImageField(upload_to='images/') 
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE, related_name='images')  
    timestamp = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"Image {self.id} for StatusMessage {self.status_message.id}"



class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)  # Store the time when friendship was created

    def __str__(self):
        return f"{self.profile1.fname} {self.profile1.lname} & {self.profile2.fname} {self.profile2.lname}"
