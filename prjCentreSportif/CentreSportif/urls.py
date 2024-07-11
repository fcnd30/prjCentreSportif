from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('register/', views.sign_up, name="sign_up"),
    path('login/', views.sign_in, name="sign_in"),
    path('log_out/', views.log_out, name="log_out"),
    path('inscription/<int:activite_id>/', views.inscription, name='inscription'),
    path('inscription_activite/<int:activite_id>/', views.inscription_activite, name='inscription_activite'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('gestion_activites/', views.gestion_activites, name='gestion_activites'),
    path('gestion_clients/', views.gestion_clients, name='gestion_clients'),
    path('admin_moniteurs/', views.admin_moniteurs, name='admin_moniteurs'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    # path('confirmation_activite/<int:inscription_id>/', views.confirmation_activite, name='confirmation_activite'),
    path('add_activite/', views.add_activite, name='add_activite'),
    path('edit_activite/<int:activite_id>/', views.edit_activite, name='edit_activite'),
    path('delete_activite/<int:activite_id>/', views.delete_activite, name='delete_activite'),
    path('gestion_inscription/', views.gestion_inscription, name='gestion_inscription'),

    path('gestion_paiements/', views.gestion_paiements, name='gestion_paiements'),
    path('gestion_moniteurs/', views.gestion_moniteurs, name='gestion_moniteurs'),
    path('gestion_horaires/', views.gestion_horaires, name='gestion_horaires'),
    path('delete_inscription/<int:inscription_id>/', views.delete_inscription, name='delete_inscription'),
    path('add_moniteur/', views.add_moniteur, name='add_moniteur'),
    path('edit_moniteur/<int:moniteur_id>/', views.edit_moniteur, name='edit_moniteur'),
    path('delete_moniteur/<int:moniteur_id>/', views.delete_moniteur, name='delete_moniteur'),
    path('gestion_horaires/', views.gestion_horaires, name='gestion_horaires'),
    path('add_horaire/', views.add_horaire, name='add_horaire'),
    path('edit_horaire/<int:horaire_id>/', views.edit_horaire, name='edit_horaire'),
    path('delete_horaire/<int:horaire_id>/', views.delete_horaire, name='delete_horaire'),
    path('apropos/', views.apropos, name="apropos"),
    
]