from django.urls import path

from . import views

app_name = 'oligos'

urlpatterns = [
    path('all/', views.ClientOrderListView.as_view(), name='client_order_list'),
    path('view/<int:pk>', views.OligoDetailView.as_view(), name='detail_view'),
    path('number/', views.OligoNewTypeView.as_view(), name='order_quantity'),
    path('create/', views.OligoCreateView.as_view(), name='order_create'),
    path('easy-order/', views.OligoEasyOrder.as_view(), name='easy_order'),
    path('easy-submit/', views.OligoEasySubmitView.as_view(), name='easy_submit'),
]