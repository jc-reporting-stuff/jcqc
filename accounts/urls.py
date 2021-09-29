from django.urls import path
from .views import AccountSignupView, EditAccountView, UpdateProfileView, UserAccountsView

urlpatterns = [
    path('signup_form/', AccountSignupView.as_view(), name='signup'),
    path('account_settings/', EditAccountView.as_view(), name='edit_account'),
    path('update_profile/<int:pk>', UpdateProfileView.as_view(), name='update_profile'),

    path('financial-accounts/', UserAccountsView.as_view(), name='view_user_accounts')
]