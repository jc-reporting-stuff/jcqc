from django.contrib.auth.decorators import login_required
from django.conf import settings

import re


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.required = (re.compile(r'^.*$'),)
        self.exceptions = tuple(re.compile(url)
                                for url in settings.LOGIN_EXEMPT_URLS)
        self.open_urls = self.exceptions

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # if authenticated return no exception
        if request.user.is_authenticated:
            return None
        # if found in allowed exceptional urls return no exception
        for url in self.open_urls:
            if url.match(request.path):
                return None

        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        return None
