from django.urls import path
from . import views
from .views import CustomLoginView, activate
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('activate/userId=<uidb64>-main-userToken=<token>/', activate, name='activate'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('download', views.downloads, name='downloads'),
    path('register', views.signup, name='signup'),
]
