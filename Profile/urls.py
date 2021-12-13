from django.urls import path, include
from django.contrib.auth import views as auth_views
from Profile.views import ( 
            UserCreateView,
            ProfileList,
            ProfileRegisterView,
            ProfilesIndexView,
            ProfileDeleteView,
            JobPositionList,
            JobPositionCreate,
            JobPositionDeleteView,
            JobPositionUpdateView,
    )
from Profile.forms import UserLoginForm


urlpatterns = [
    # Pre defined Views
    path('login/', auth_views.LoginView.as_view(template_name="profile/login.html",
                                                authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # User | Profile Creation
    path('user/register/', UserCreateView.as_view(), name="register"),
    path('profile/update/<slug>/',ProfileRegisterView.as_view(),name='profile-update'),
    # Profile Management
    path('profiles/',ProfilesIndexView.as_view(),name='profiles'),
    path('profile/delete/<slug>/',ProfileDeleteView.as_view(),name='profile-delete'),
    path('profiles-list/', ProfileList.as_view(), name="profiles-list"),
    # Job Position List
    path('job-positions/',JobPositionList.as_view(),name='job-position'),
    path('job-position/create/',JobPositionCreate.as_view(),name='job-position-create'),
    path('jobposition/delete/<slug>/',JobPositionDeleteView.as_view(),name='jobposition-delete'),
    path('jobposition/update/<slug>/',JobPositionUpdateView.as_view(),name='jobposition-update'),

]
