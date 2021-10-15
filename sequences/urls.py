from django.urls import path

from . import views

app_name = 'sequencing'

urlpatterns = [
    path('', views.MethodSelectView, name='choose_method'),
    path('template/add/', views.TemplateAddView, name='add_templates'),
    path('template/view/<int:pk>/',
         views.TemplateDetailView.as_view(), name='template_detail'),
    path('primer/view/<int:pk>/',
         views.PrimerDetailView.as_view(), name='primer_detail'),
    path('primer/add/', views.PrimerAddView, name='add_primers'),
    path('reaction/add/', views.ReactionAddView, name='add_reactions'),
    path('reaction/list/', views.ReactionListView.as_view(), name='list_reactions'),
]
