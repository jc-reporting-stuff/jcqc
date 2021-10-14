from django.views.generic import TemplateView
from django.shortcuts import render

from django.http import HttpResponseRedirect

import requests


class HomePageView(TemplateView):
    template_name = 'home.html'


def VizHomeView(request):
    if request.method == 'GET':
        return render(request, 'get_username.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        server_url = 'http://131.104.184.6/trusted'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        client_ip = request.META.get('REMOTE_ADDR')
        data = {'username': username, 'client_ip': client_ip}
        r = requests.post(
            server_url,
            headers=headers,
            data=data)

        ticket = r.text

        url = f'http://131.104.184.6/trusted/{ticket}/views/TestData/DummyData'

        context = {
            'ticket': ticket
        }
        # return render(request, 'viz_main.html', context=context)
        return HttpResponseRedirect(url)
