from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from .models import StatusMessage, Image, Profile
from django import forms


class ShowAllProfilesView(ListView):
    template_name = 'mini_fb/show_all_profiles.html'
    model = Profile
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'  
    context_object_name = 'profile'  


from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'  
    
    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])


from django.shortcuts import redirect
from .models import Profile, StatusMessage, Image

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        """
        Save the StatusMessage and handle the image upload.
        """
        # Save the form, which will save the StatusMessage
        sm = form.save(commit=False)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        sm.profile = profile
        sm.save()

        # Read the files from the request
        files = self.request.FILES.getlist('files')  # Get the list of uploaded files

        # Process each file and create Image objects
        for file in files:
            image = Image(
                image_file=file,
                status_message=sm  # Link the image to the status message
            )
            image.save()

        return redirect('show_profile', pk=profile.pk)

    def get_context_data(self, **kwargs):
        """
        Add the profile to the context.
        """
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def get_success_url(self):
        return reverse('show_profile', args=[self.kwargs['pk']])
    
    
class StatusMessageForm(forms.ModelForm):
    '''Form to post a new StatusMessage, with an option to add an image.'''
    
    image_file = forms.ImageField(required=False)
    
    class Meta:
        model = StatusMessage
        fields = ['message']  