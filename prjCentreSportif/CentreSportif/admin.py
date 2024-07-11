from django.contrib import admin
from .models import Client, Activite, Inscription, Paiement, Moniteur, Horaire

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom_client', 'prenom_client', 'username', 'email', 'age', 'choix_sport', 'role')
    search_fields = ('nom_client', 'prenom_client', 'email')

class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom_activite', 'categories', 'prix', 'image')
    search_fields = ('nom_activite',)

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'activite', 'date_inscription', 'statut_inscription', 'horaire')
    list_filter = ('statut_inscription', 'date_inscription')
    search_fields = ('client__nom_client', 'client__prenom_client', 'activite__nom_activite')

class PaiementAdmin(admin.ModelAdmin):
    list_display = ('inscription', 'montant', 'date_paiement', 'mode_paiement')
    list_filter = ('date_paiement', 'mode_paiement')
    search_fields = ('inscription__client__nom_client', 'inscription__client__prenom_client')

class MoniteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')
    search_fields = ('nom', 'prenom', 'email')

class HoraireAdmin(admin.ModelAdmin):
    list_display = ('activite', 'jour', 'heure_debut', 'heure_fin', 'moniteur')
    list_filter = ('jour', 'heure_debut', 'heure_fin')
    search_fields = ('moniteur__nom', 'moniteur__prenom', 'activite__nom_activite')

admin.site.register(Client, ClientAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Moniteur, MoniteurAdmin)
admin.site.register(Horaire, HoraireAdmin)
