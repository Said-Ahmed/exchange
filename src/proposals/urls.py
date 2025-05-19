from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('', views.all_proposals, name='all_proposals'),
    path('create/', views.create_exchange_proposal, name='create_proposal'),
    path('<int:pk>/update/<str:new_status>/', views.update_proposal_status, name='update_status'),
]