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



class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        """
        Add the profile to the context.
        """
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        
        # Save the status message first
        response = super().form_valid(form)
        
        # Handle the file upload if an image is uploaded
        if self.request.FILES.get('image_file'):
            image = Image(
                image_file=self.request.FILES['image_file'],
                status_message=form.instance  # Link the image to the newly created status message
            )
            image.save()
        
        return response

    def get_success_url(self):
        return reverse('show_profile', args=[self.kwargs['pk']])
class StatusMessageForm(forms.ModelForm):
    '''Form to post a new StatusMessage, with an option to add an image.'''
    
    # Add an image field (not required)
    image_file = forms.ImageField(required=False)
    
    class Meta:
        model = StatusMessage
        fields = ['message']  # Include only the message field