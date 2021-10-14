from django.views.generic import TemplateView
from django.shortcuts import render

import requests


class HomePageView(TemplateView):
    template_name = 'home.html'


def VizHomeView(request):
    server_url = 'http://131.104.184.6/trusted'
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    client_ip = request.META.get('REMOTE_ADDR')
    data = {'username': 'TU1', 'client_ip': client_ip}
    r = requests.post(
        server_url,
        headers=headers,
        data=data)

    context = {
        'server_url': server_url,
        'headers': headers,
        'data': data,
        'response': r
    }
    return render(request, 'viz_main.html', context=context)
