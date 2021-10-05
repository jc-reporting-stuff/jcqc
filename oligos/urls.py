from django.urls import path

from . import views

app_name = 'oligos'

urlpatterns = [
    path('all/', views.ClientOrderListView.as_view(), name='client_order_list'),
    path('number/', views.OligoNewTypeView.as_view(), name='order_quantity'),
    path('create/', views.OligoCreateView.as_view(), name='order_create')
]