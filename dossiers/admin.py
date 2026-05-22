from django.contrib import admin
from .models import Client, Dossier, Intervention , Audience, Document

# ==========================================
# 1. ADMIN CLIENT
# ==========================================
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'telephone', 'date_ajout')
    search_fields = ('nom', 'prenom', 'telephone')

# ==========================================
# 2. ADMIN DOSSIER (Hna fin kan l-moshkil)
# ==========================================
@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    # 7iyedna 'avocat' w 'date_creation' 7it makayninch f models.py
    list_display = ('id', 'titre', 'client', 'type_affaire', 'statut') 
    
    # 7iyedna 'avocat' mn l-filtre
    list_filter = ('statut', 'type_affaire') 
    
    # Zedna recherche l-Avocat y-qelleb b Titre wla b Smiyt l'Client
    search_fields = ('titre', 'client__user__username', 'client__user__first_name')

# ==========================================
# 3. ADMIN L-KHRIN (Interventions, Audiences...)
# ==========================================
@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_intervention')

@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'tribunal', 'date_audience')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_creation')