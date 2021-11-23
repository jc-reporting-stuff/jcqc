from django.urls import path

from . import views

app_name = 'oligos'

urlpatterns = [
    path('all/', views.ClientOrderListView.as_view(), name='client_order_list'),
    path('view/<int:pk>', views.OligoDetailView.as_view(), name='detail_view'),
    path('list/<str:username>', views.UserListView.as_view(), name='user_orders'),
    path('number/', views.OligoNewTypeView.as_view(), name='order_quantity'),
    path('create/', views.OligoCreateView.as_view(), name='order_create'),
    path('easy-order/', views.OligoEasyOrder.as_view(), name='easy_order'),
    path('easy-submit/', views.OligoEasySubmitView.as_view(), name='easy_submit'),
    path('admin/today/', views.OligoTodayListView.as_view(), name='today_listview'),
    path('admin/', views.OligoAdminHomeView.as_view(), name='admin_home'),
    path('search/', views.OligoSearchView.as_view(), name='search'),
    path('search-results/', views.OligoListView.as_view(), name='search_results'),
    path('list-actions/', views.OligoListActionsView.as_view(), name='list_actions'),
    path('billing/', views.BillingView.as_view(), name='billing'),
    path('bankfile/', views.BankfileDownload.as_view(), name='bankfile'),
    path('od/', views.EnterODView.as_view(), name='enter_od'),
    path('report/', views.ReportOrderView, name='report'),
    path('remove/', views.RemoveOrderView.as_view(), name='remove'),
]
