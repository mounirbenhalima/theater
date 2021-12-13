from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from django.utils.decorators import method_decorator
from . models import Profile, JobPosition
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    View
)

from .forms import UserCreationForm, UserRegisterForm, ProfileForm, JobPositionForm
from django.template.defaultfilters import slugify


class ProfilesIndexView(View):
    template_name = 'profile/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'profile/add_update/user_add.html'

    def get_success_url(self):
        return reverse('profile-update', kwargs={
            "slug": self.object.profile.slug
        })

class ProfileRegisterView(UpdateView):
    template_name = 'profile/add_update/profile_update.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profiles-list')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=_slug)


class ProfileList(ListView):
    model = Profile
    #queryset = Profile.objects.all()
    template_name = 'profile/list/profile_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
        else:
            object_list = self.model.objects.all()
        return object_list

class ProfileDeleteView(DeleteView):
    template_name = 'profile/delete/profile_delete.html'
    success_url = reverse_lazy('profiles-list')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=_slug)


class JobPositionList(ListView):
    template_name = 'profile/list/job_position_list.html'
    queryset = JobPosition.objects.all()


class JobPositionCreate(CreateView):
    model = JobPosition
    template_name = 'profile/add_update/job_position_add.html'
    form_class = JobPositionForm
    success_url = reverse_lazy('job-position')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class JobPositionDeleteView(DeleteView):
    template_name = 'profile/delete/jobposition_delete.html'
    success_url = reverse_lazy('job-position')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(JobPosition, slug=_slug)

class JobPositionUpdateView(UpdateView):
    template_name = 'profile/add_update/jobposition_update.html'
    form_class = JobPositionForm
    success_url = reverse_lazy('job-position')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        _slug = self.kwargs.get('slug')
        return get_object_or_404(JobPosition, slug=_slug)

# TODO CBV
def login_view(request):
    return render(request, "profile/login.html")
