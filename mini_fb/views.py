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
    template_name = 'mini_fb/show_profile.html'  # Points to the template for showing a profile
    context_object_name = 'profile'  # The context name for the Profile object
