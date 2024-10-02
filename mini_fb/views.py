from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'
