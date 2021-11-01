from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import HomePageView, ClientListView

urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('client-list/', ClientListView.as_view(), name='client_list')
]
