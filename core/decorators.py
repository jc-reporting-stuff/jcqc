from django.contrib import messages
from django.shortcuts import redirect, reverse


def user_has_accounts(function):
    def wrap(request, *args, **kwargs):
        accounts = request.user.get_financial_accounts()
        user = request.user

        if len(accounts) == 0:
            messages.info(
                request, r'You must have a financial account in place to order things.')
            if user.is_student:
                redirect_target = 'student_supervisor_request'
            else:
                redirect_target = 'view_user_accounts'
            return redirect(reverse(redirect_target))
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap


def owner_or_staff(function):
    def wrap(request, *args, **kwargs):
        requested_user = kwargs.pop('username')

        if (not request.user.is_staff or not request.user.is_superuser) and request.user.username != requested_user:
            messages.warning(
                request, 'You are not authorized to view that page.')
            redirect_target = 'oligos:client_order_list'
            return redirect(reverse(redirect_target))

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap
