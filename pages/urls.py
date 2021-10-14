from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePageView, VizHomeView

urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('disease-surveillance/', VizHomeView, name='viz_home')
]
