from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile
from .forms import ContactForm, UserProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

class RegisterView(CreateView) :
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)
    

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
           
#     else:
#         form = ContactForm()
#     return render(request, 'message/contact.html', {'form': form})

class ContactView(FormView) :
    form_class = ContactForm
    template_name = 'message/contact.html'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        return super().form_valid(form)

@login_required
def profile(request) :
    user_profile, created = UserProfile.objects.get_or_create() 
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile
        )

        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()

            return redirect('profile')  
        
    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', {'u_form' : u_form, 'p_form' : p_form})



# class ProfileView(LoginRequiredMixin, View) :
#     template_name = 'users/profile.html'

#     def get(self, request, *args, **kwargs) :
#         user_profile, created = UserProfile.objects.get_or_create(user = request.user)
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = UserProfileForm(instance=user_profile)
#         return render(request, self.template_name, {'u_form' : u_form, 'p_form' : p_form})
#     def post(self, request, *args, **kwargs) :
#         user_profile, created = UserProfile.objects.get_or_create(user = request.user)
#         u_form =UserUpdateForm(request.POST, instance=request.user)
#         p_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             return redirect('profile')
#         return render(request, self.template_name, {'u_form': u_form, 'p_form': p_form})
