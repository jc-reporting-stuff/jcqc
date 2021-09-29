from django.urls import path
from .views import AccountSignupView, EditAccountView, UpdateProfileView, UserAccountsView, RequestSupervisorView

urlpatterns = [
    path('signup_form/', AccountSignupView.as_view(), name='signup'),
    path('account_settings/', EditAccountView.as_view(), name='edit_account'),
    path('update_profile/<int:pk>', UpdateProfileView.as_view(), name='update_profile'),

    path('financial-accounts/', UserAccountsView.as_view(), name='view_user_accounts'),
    path('request-preapproval/', RequestSupervisorView.as_view(), name='student_supervisor_request')
]