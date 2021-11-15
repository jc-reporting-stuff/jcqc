from django.urls import path

from . import views

app_name = 'sequencing'

urlpatterns = [
    path('', views.MethodSelectView, name='method_select'),
    path('list/<str:username>', views.UserListView.as_view(), name='user_orders'),
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
    path('today/', views.SequencesTodayListView.as_view(), name='today_listview'),
    path('search/', views.SequenceSearchView.as_view(), name='search'),
    path('search-results/', views.SequenceListView.as_view(), name='search_results'),
    path('list-actions', views.SequenceListActionsView.as_view(), name='list_actions'),
    path('billing/', views.BillingView.as_view(), name='billing'),
    path('prep/menu/', views.PrepMenuView.as_view(), name='prep_menu'),
    path('remove/', views.RemoveOrderView.as_view(), name='remove'),

    path('worksheet/<str:name>/<int:block>', views.WorksheetDetailView.as_view(),
         name='worksheet_detail'),
    path('worksheet/edit/<str:name>/<int:block>', views.WorksheetEditView.as_view(),
         name='worksheet_edit'),
    path('worksheet/search/', views.WorksheetSearchView.as_view(),
         name='worksheet_search'),
    path('worksheet/add/', views.WorksheetAddView.as_view(),
         name='worksheet_add'),
    path('worksheet/submit/', views.WorksheetSubmitView.as_view(),
         name='worksheet_submit'),
    path('worksheet/list/', views.WorksheetListView.as_view(),
         name='worksheet_list'),
    path('worksheet/active/<int:pk>/', views.WorksheetToggleActiveView.as_view(),
         name='worksheet_toggle_active'),
    path('worksheet/preview/', views.WorksheetPreviewView.as_view(),
         name='worksheet_preview'),
    path('worksheet/update/well/', views.WorksheetUpdateWellView.as_view(),
         name='worksheet_update_well'),

    path('runfile/create/', views.RunfileCreateView.as_view(),
         name='runfile_create'),
]
