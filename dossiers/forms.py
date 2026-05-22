from django import forms
from .models import Dossier, Document, Client, Intervention, Audience

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['titre', 'client', 'type_affaire', 'statut', 'partie_adverse', 'tribunal', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'fichier']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['prenom', 'nom', 'telephone', 'adresse', 'photo_cin']

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ['titre', 'description', 'date_intervention', 'document_joint']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date_intervention': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['dossier', 'date_audience', 'tribunal', 'salle', 'notes']
        widgets = {
            'date_audience': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
