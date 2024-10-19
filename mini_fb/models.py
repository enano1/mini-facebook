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



