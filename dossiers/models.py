from django.db import models
from django.conf import settings

class Client(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    photo_cin = models.ImageField(upload_to='clients/cin/', null=True, blank=True, verbose_name="Photo CIN")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom.title()} {self.nom.upper()}"

class Dossier(models.Model):
    TYPE_CHOICES = [
        ('Civil', 'Droit Civil'),
        ('Penal', 'Droit Pénal'),
        ('Commercial', 'Droit Commercial'),
        ('Famille', 'Droit de la Famille'),
        ('Travail', 'Droit du Travail'),
        ('Administratif', 'Droit Administratif'),
        ('Autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('En cours', 'En cours'),
        ('Clôturé', 'Clôturé'),
        ('Archivé', 'Archivé'),
    ]

    titre = models.CharField(max_length=200)
    
    # Hna daba Django ghay-3ref chno howa 'Client' 7it mktoub l-fouq
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='dossiers')
    
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='En cours')
    type_affaire = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Civil')
    partie_adverse = models.CharField(max_length=200, blank=True, null=True, verbose_name="Partie Adverse ")
    tribunal = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tribunal Compétent")
    description = models.TextField(blank=True, null=True, verbose_name="Résumé des Faits")
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.titre} - {self.client}"

class Intervention(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='interventions')
    titre = models.CharField(max_length=250)
    description = models.TextField()
    document_joint = models.FileField(upload_to='interventions/documents/', null=True, blank=True)
    date_intervention = models.DateTimeField()

    def __str__(self):
        return f"{self.titre} - {self.dossier.titre}"

class Audience(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='audiences')
    date_audience = models.DateTimeField()
    tribunal = models.CharField(max_length=150)
    salle = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Audience: {self.tribunal} - {self.dossier.titre}"

class Document(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=250)
    fichier = models.FileField(upload_to='dossiers/documents/' , null=True, blank=True) 
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre