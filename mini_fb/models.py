from django.db import models

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
    

