from django.core.management.base import BaseCommand
from faker import Faker
import random
import datetime

from dossiers.models import Client, Dossier, Intervention, Audience, Document

class Command(BaseCommand):
    help = 'Génère des fausses données marocaines pour le cabinet'

    def handle(self, *args, **options):

        # ---------------------------------------------------------
        # Données marocaines
        # ---------------------------------------------------------
        prenoms = ['Youssef', 'Mohammed', 'Fatima', 'Aicha', 'Omar', 'Khalid',
                   'Nadia', 'Hamid', 'Zineb', 'Rachid', 'Samira', 'Karim',
                   'Houda', 'Tariq', 'Meryem', 'Amine', 'Loubna', 'Hassan',
                   'Imane', 'Soufiane']

        noms = ['Benali', 'El Fassi', 'Idrissi', 'Benjelloun', 'Tahiri',
                'Cherkaoui', 'Bouazza', 'El Amrani', 'Kettani', 'Bensalah',
                'Ouali', 'Chraibi', 'Tazi', 'Lahlou', 'Berrada',
                'El Ouazzani', 'Skalli', 'Filali', 'Ghazali', 'Ziani']

        villes = ['Casablanca', 'Rabat', 'Marrakech', 'Fès', 'Tanger',
                  'Agadir', 'Meknès', 'Oujda', 'Kénitra', 'Tétouan']

        tribunaux = [
            'Tribunal de Première Instance de Casablanca',
            'Tribunal de Commerce de Casablanca',
            'Tribunal de Première Instance de Rabat',
            'Tribunal Administratif de Rabat',
            'Tribunal de Première Instance de Marrakech',
            'Tribunal de Commerce de Tanger',
            'Tribunal de Première Instance de Fès',
            'Cour d\'Appel de Casablanca',
            'Cour d\'Appel de Rabat',
            'Tribunal de Première Instance d\'Agadir',
        ]

        titres_dossiers = [
            'Litige foncier - Terrain agricole',
            'Divorce par consentement mutuel',
            'Recouvrement de créances commerciales',
            'Accident de travail - Indemnisation',
            'Contentieux locatif - Expulsion',
            'Héritage et partage de succession',
            'Licenciement abusif',
            'Escroquerie et abus de confiance',
            'Litige commercial entre associés',
            'Pension alimentaire et garde d\'enfants',
            'Construction sans permis',
            'Diffamation et atteinte à l\'honneur',
            'Contrat de vente immobilière contesté',
            'Détournement de fonds',
            'Violence conjugale',
            'Litige douanier',
            'Impayés de loyer commercial',
            'Faillite et liquidation judiciaire',
            'Contestation de testament',
            'Infractions au code de la route',
        ]

        titres_interventions = [
            'Réunion de consultation avec le client',
            'Dépôt du dossier au tribunal',
            'Plaidoirie en première instance',
            'Constitution du dossier de preuves',
            'Négociation avec la partie adverse',
            'Rédaction des conclusions',
            'Demande de renvoi d\'audience',
            'Expertise judiciaire demandée',
            'Notification du jugement',
            'Appel du jugement déposé',
        ]

        parties_adverses = [
            'Société ATLAS IMMO SARL',
            'M. Rachid Bennani',
            'Banque Populaire du Maroc',
            'Société Générale Maroc',
            'Mme Fatima Zerhouni',
            'Municipalité de Casablanca',
            'Agence Nationale de l\'Immobilier',
            'M. Karim El Fassi',
            'Compagnie d\'Assurance WAFA',
            'Société MAGHREB TRANSIT',
        ]

        # ---------------------------------------------------------
        # 1. Créer 10 clients marocains
        # ---------------------------------------------------------
        clients_crees = []
        for i in range(10):
            prenom = random.choice(prenoms)
            nom = random.choice(noms)
            ville = random.choice(villes)
            telephone = f"06{random.randint(10000000, 99999999)}"
            adresse = f"{random.randint(1, 200)} Rue {random.choice(['Hassan II', 'Mohammed V', 'Al Massira', 'Ibn Sina', 'Al Fida'])}, {ville}"

            client = Client.objects.create(
                prenom=prenom,
                nom=nom,
                telephone=telephone,
                adresse=adresse,
            )
            clients_crees.append(client)
            self.stdout.write(f"✔ Client créé : {prenom} {nom.upper()} — {telephone}")

        # ---------------------------------------------------------
        # 2. Créer 20 dossiers
        # ---------------------------------------------------------
        statuts = ['En cours', 'En cours', 'En cours', 'Clôturé', 'Archivé']
        types = ['Civil', 'Penal', 'Commercial', 'Famille', 'Travail', 'Administratif']

        random.shuffle(titres_dossiers)

        for i, titre in enumerate(titres_dossiers):
            client = random.choice(clients_crees)
            tribunal = random.choice(tribunaux)

            dossier = Dossier.objects.create(
                titre=titre,
                client=client,
                statut=random.choice(statuts),
                type_affaire=random.choice(types),
                partie_adverse=random.choice(parties_adverses),
                tribunal=tribunal,
                description=random.choice([
                    f"Le client {client.prenom} {client.nom} a saisi le cabinet suite à un différend portant sur {titre.lower()}. Les faits remontent à plusieurs mois et nécessitent une intervention urgente.",
                    f"Affaire complexe impliquant plusieurs parties. Le client conteste la décision rendue et souhaite faire appel.",
                    f"Dossier en cours d'instruction. Les pièces justificatives ont été rassemblées et le dossier est prêt pour l'audience.",
                ])
            )

            # 1 à 3 interventions par dossier
            nb_interventions = random.randint(1, 3)
            for _ in range(nb_interventions):
                Intervention.objects.create(
                    dossier=dossier,
                    titre=random.choice(titres_interventions),
                    description=f"Intervention réalisée dans le cadre du dossier {dossier.titre[:40]}. Toutes les parties ont été informées.",
                    date_intervention=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=random.randint(1, 180)),
                )

            # 1 audience par dossier (passée ou à venir)
            jours = random.randint(-30, 120)
            Audience.objects.create(
                dossier=dossier,
                date_audience=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=jours),
                tribunal=tribunal,
                salle=f"Salle {random.randint(1, 15)}",
                notes=random.choice([
                    "Présence obligatoire des deux parties.",
                    "Expertise demandée par le juge.",
                    "Renvoi possible si dossier incomplet.",
                    "Jugement attendu à cette date.",
                    "",
                ])
            )

            # 1 document par dossier
            Document.objects.create(
                dossier=dossier,
                titre=random.choice([
                    'Copie CIN client',
                    'Contrat signé',
                    'Jugement de première instance',
                    'Acte de naissance',
                    'Titre foncier',
                    'Procès verbal',
                    'Attestation de travail',
                    'Relevé bancaire',
                ])
            )

            self.stdout.write(f"✔ Dossier {i+1}/20 créé : {titre[:50]}")

        self.stdout.write(self.style.SUCCESS('\n Données générées avec succès !'))