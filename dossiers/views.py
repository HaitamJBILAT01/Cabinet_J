from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Dossier, Client, Intervention, Audience, Document
from .forms import DossierForm, DocumentForm, ClientForm, InterventionForm, AudienceForm
from datetime import date
from django.db.models import Q
from .mixins import AvocatRequiredMixin

# ==========================================
# 1. PAGES PRINCIPALES
# ==========================================
def landing_page(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    total_dossiers = Dossier.objects.count()
    dossiers_en_cours = Dossier.objects.filter(statut='En cours').count()
    total_clients = Client.objects.count()
    prochaine_intervention = Intervention.objects.filter(date_intervention__gte=date.today()).order_by('date_intervention').first()
    dossiers_recents = Dossier.objects.all().order_by('-id')[:5]
    prochaines_audiences = Audience.objects.filter(date_audience__gte=date.today()).order_by('date_audience')[:5]
    total_audiences = Audience.objects.filter(date_audience__gte=date.today()).count()

    context = {
        'total_dossiers': total_dossiers,
        'dossiers_en_cours': dossiers_en_cours,
        'total_clients': total_clients,
        'prochaine_intervention': prochaine_intervention,
        'dossiers_recents': dossiers_recents,
        'prochaines_audiences': prochaines_audiences,
        'total_audiences': total_audiences,
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. VUES DES DOSSIERS & CLIENTS
# ==========================================
class DossierListView(LoginRequiredMixin, ListView):
    model = Dossier
    template_name = 'dossiers/dossier_list.html'
    context_object_name = 'dossiers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Dossier.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titre__icontains=query) |
                Q(client__nom__icontains=query) |
                Q(client__prenom__icontains=query) |
                Q(partie_adverse__icontains=query)
            )
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        type_affaire = self.request.GET.get('type')
        if type_affaire:
            queryset = queryset.filter(type_affaire=type_affaire)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_statut'] = self.request.GET.get('statut', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['type_choices'] = Dossier.TYPE_CHOICES
        return context

class DossierDetailView(LoginRequiredMixin, DetailView):
    model = Dossier
    template_name = 'dossiers/dossier_detail.html'
    context_object_name = 'dossier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['intervention_form'] = InterventionForm()
        return context

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'dossiers/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = Client.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) |
                Q(prenom__icontains=query) |
                Q(telephone__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'dossiers/client_detail.html'
    context_object_name = 'client'

# ==========================================
# 3. AJOUT & MODIFICATION
# ==========================================
class DossierCreateView(LoginRequiredMixin, CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'
    success_url = reverse_lazy('dossier_list')

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get('client')
        if client_id:
            initial['client'] = client_id
        return initial

class DossierUpdateView(LoginRequiredMixin, UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'

    def get_success_url(self):
        return reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class DossierDeleteView(LoginRequiredMixin, AvocatRequiredMixin, DeleteView):
    model = Dossier
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('dossier_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'le dossier'
        context['object_name'] = self.object.titre
        context['cancel_url'] = reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})
        return context




class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class ClientDeleteView(LoginRequiredMixin, AvocatRequiredMixin, DeleteView):
    model = Client
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'le client'
        context['object_name'] = str(self.object)
        context['cancel_url'] = reverse_lazy('client_detail', kwargs={'pk': self.object.pk})
        return context

# ==========================================
# 4. DOCUMENTS & INTERVENTIONS
# ==========================================
@login_required
def importer_document(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.dossier = dossier
            document.save()
            messages.success(request, 'Document importé avec succès.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def supprimer_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    dossier_pk = document.dossier.pk
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé.')
    return redirect('dossier_detail', pk=dossier_pk)

@login_required
def ajouter_intervention(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = InterventionForm(request.POST, request.FILES)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.dossier = dossier
            intervention.save()
            messages.success(request, 'Intervention ajoutée avec succès.')
    return redirect('dossier_detail', pk=pk)

@login_required
def supprimer_intervention(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    dossier_pk = intervention.dossier.pk
    if request.method == 'POST':
        intervention.delete()
        messages.success(request, 'Intervention supprimée.')
    return redirect('dossier_detail', pk=dossier_pk)

# ==========================================
# 5. AUDIENCES
# ==========================================
class AudienceListView(LoginRequiredMixin, ListView):
    model = Audience
    template_name = 'dossiers/audience_list.html'
    context_object_name = 'audiences'
    paginate_by = 15

    def get_queryset(self):
        queryset = Audience.objects.all().order_by('date_audience')
        filtre = self.request.GET.get('filtre', 'toutes')
        if filtre == 'a_venir':
            queryset = queryset.filter(date_audience__gte=date.today())
        elif filtre == 'passees':
            queryset = queryset.filter(date_audience__lt=date.today())
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(tribunal__icontains=query) |
                Q(dossier__titre__icontains=query) |
                Q(dossier__client__nom__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtre'] = self.request.GET.get('filtre', 'toutes')
        context['search_query'] = self.request.GET.get('q', '')
        context['today'] = date.today()
        return context

class AudienceCreateView(LoginRequiredMixin, CreateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'dossiers/audience_form.html'
    success_url = reverse_lazy('audience_list')

    def get_initial(self):
        initial = super().get_initial()
        dossier_id = self.request.GET.get('dossier')
        if dossier_id:
            initial['dossier'] = dossier_id
        return initial

class AudienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Audience
    form_class = AudienceForm
    template_name = 'dossiers/audience_form.html'
    success_url = reverse_lazy('audience_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class AudienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Audience
    template_name = 'dossiers/confirm_delete.html'
    success_url = reverse_lazy('audience_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = "l'audience"
        context['object_name'] = f"{self.object.tribunal} — {self.object.date_audience.strftime('%d/%m/%Y')}"
        context['cancel_url'] = reverse_lazy('audience_list')
        return context
