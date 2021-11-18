from django.views.generic import TemplateView, ListView
from allauth.account.views import LoginView

from accounts.models import User
from pages.models import Message


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class MoreInfoView(TemplateView):
    template_name = 'pages/info.html'


class ClientListView(ListView):
    template_name = 'pages/client_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by')
        else:
            order_by = 'last_name'
        return User.objects.all().order_by(order_by)


class MessageLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = Message.objects.get(name='FrontPageMessage')
        context['message'] = message
        return context
