from django.views.generic import TemplateView
from django.shortcuts import render

from django.http import HttpResponseRedirect

import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ticket(username, ip_address):
    server_url = 'http://131.104.184.6/trusted'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    data = {'username': username, 'client_ip': ip_address}
    r = requests.post(
        server_url,
        headers=headers,
        data=data)

    return r.text


class HomePageView(TemplateView):
    template_name = 'home.html'


def VizHomeView(request):

    username = 'TU1'
    client_ip = get_client_ip(request)
    data = {'username': username, 'client_ip': client_ip}

    ticket = get_ticket(username, client_ip)
    ticket2 = get_ticket(username, client_ip)

    # Each viz needs its own ticket.
    context = {
        'ticket': ticket,
        'ticket2': ticket2
    }
    return render(request, 'viz_main.html', context=context)
    # return HttpResponseRedirect(url)
