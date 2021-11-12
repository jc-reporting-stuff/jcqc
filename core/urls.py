
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('oliseq-admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),
    path('user/', include('accounts.urls')),

    # Oligos orders
    path('oligos/', include('oligos.urls')),

    # Sequencing submissions
    path('sequences/', include('sequences.urls')),

    # Local apps
    path('', include('pages.urls')),
]

admin.site.site_header = "Oligo and Sequencing Admin"
admin.site.site_title = "Website Admin Portal"
admin.site.index_title = "Welcome to Oligo and Sequencing Admin Portal"
