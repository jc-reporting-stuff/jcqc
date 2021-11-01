from django.views.generic import TemplateView, ListView
from django.shortcuts import render

from accounts.models import User


class HomePageView(TemplateView):
    template_name = 'home.html'


class ClientListView(ListView):
    template_name = 'pages/client_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by')
        else:
            order_by = 'last_name'
        return User.objects.all().order_by(order_by)
