from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import CreateView

from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
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


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'  
    
    def get_success_url(self):
        return reverse('show_profile', args=[self.object.pk])


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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_success_url(self):
        """
        After updating the profile, redirect back to the profile page.
        """
        return reverse('show_profile', args=[self.object.pk])

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        """
        Redirect back to the profile page after deleting the status message.
        """
        profile_pk = self.object.profile.pk  
        return reverse('show_profile', args=[profile_pk])

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']  
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        """
        Redirect back to the profile page after updating the status message.
        """
        profile_pk = self.object.profile.pk  
        return reverse('show_profile', args=[profile_pk])

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from .models import Profile

class CreateFriendView(View):
    """A view to add a friend to the profile."""

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])  # The profile doing the adding
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])  # The profile being added as a friend

        profile.add_friend(other_profile)

        messages.success(request, f'You are now friends with {other_profile.fname} {other_profile.lname}!')

        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context


class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news_feed'] = self.object.get_news_feed()
        return context

