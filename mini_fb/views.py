from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'

from django.views.generic.detail import DetailView

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'  
    context_object_name = 'profile'  


# In mini_fb/views.py
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'  
    
    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])
