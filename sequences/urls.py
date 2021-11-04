from django.urls import path

from . import views

app_name = 'sequencing'

urlpatterns = [
    path('', views.MethodSelectView, name='method_select'),
    path('template/view/<int:pk>/',
         views.TemplateDetailView.as_view(), name='template_detail'),
    path('primer/view/<int:pk>/',
         views.PrimerDetailView.as_view(), name='primer_detail'),
    path('primer/common/', views.CommonPrimerView.as_view(), name='common_primers'),
    path('reaction/add/', views.ReactionAddView, name='add_reactions'),
    path('reaction/bulk/', views.BulkReactionAddView.as_view(),
         name='add_bulk_reactions'),
    path('reaction/list/', views.ReactionListView.as_view(), name='list_reactions'),
    path('submission/<int:submission_id>', views.SubmissionDetailView.as_view(),
         name='submission_detail'),
    path('sequencing-admin/',
         views.SequencingAdminHomeView.as_view(), name='admin_home'),
    path('today', views.SequencesTodayListView.as_view(), name='today_listview'),
    path('search', views.SequenceSearchView.as_view(), name='search'),
    path('search-results', views.SequenceListView.as_view(), name='search_results'),
    path('billing', views.BillingView.as_view(), name='billing'),
    path('prep/menu', views.PrepMenuView.as_view(), name='prep_menu'),
    path('remove', views.RemoveOrderView.as_view(), name='remove'),
]
