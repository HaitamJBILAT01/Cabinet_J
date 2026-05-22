from django.contrib import admin
from django.urls import path
from dossiers.views import (
    dashboard, DossierListView, DossierDetailView, DossierCreateView, DossierUpdateView, DossierDeleteView,
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    AudienceListView, AudienceCreateView, AudienceUpdateView, AudienceDeleteView,
    importer_document, supprimer_document, ajouter_intervention, supprimer_intervention,
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login is now the homepage
    path('', auth_views.LoginView.as_view(template_name='comptes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Dossiers
    path('dossiers/', DossierListView.as_view(), name='dossier_list'),
    path('dossier/<int:pk>/', DossierDetailView.as_view(), name='dossier_detail'),
    path('dossier/ajouter/', DossierCreateView.as_view(), name='dossier_create'),
    path('dossier/<int:pk>/modifier/', DossierUpdateView.as_view(), name='dossier_update'),
    path('dossier/<int:pk>/supprimer/', DossierDeleteView.as_view(), name='dossier_delete'),

    # Documents & Interventions
    path('dossier/<int:pk>/importer/', importer_document, name='importer_document'),
    path('document/<int:pk>/supprimer/', supprimer_document, name='supprimer_document'),
    path('dossier/<int:pk>/intervention/ajouter/', ajouter_intervention, name='ajouter_intervention'),
    path('intervention/<int:pk>/supprimer/', supprimer_intervention, name='supprimer_intervention'),

    # Clients
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/ajouter/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/modifier/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/supprimer/', ClientDeleteView.as_view(), name='client_delete'),

    # Audiences
    path('audiences/', AudienceListView.as_view(), name='audience_list'),
    path('audience/ajouter/', AudienceCreateView.as_view(), name='audience_create'),
    path('audience/<int:pk>/modifier/', AudienceUpdateView.as_view(), name='audience_update'),
    path('audience/<int:pk>/supprimer/', AudienceDeleteView.as_view(), name='audience_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)