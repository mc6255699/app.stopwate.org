from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, Count
from django.contrib import messages
from .models import *
from .forms import *



# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the terrordrome")

class ContactListView(ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"
    paginate_by = None  # client-side paging

    def get_queryset(self):
        qs = (super().get_queryset()
              .select_related("organization", "owner")
              .order_by("last_name", "first_name"))

        name = (self.request.GET.get("name") or "").strip()
        org_id = self.request.GET.get("organization")

        if name:
            # match first OR last; split words to be forgiving
            for token in name.split():
                qs = qs.filter(
                    models.Q(first_name__icontains=token) |
                    models.Q(last_name__icontains=token)
                )
        if org_id:
            qs = qs.filter(organization_id=org_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = ContactFilterForm(self.request.GET)
        return ctx
class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'  # create this template
    context_object_name = 'contact'

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'  # your crispy form template
    success_url = reverse_lazy('contacts:list')

    def form_valid(self, form):
        # Automatically assign owner as logged-in user if not set
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)
    
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'  # reuse create template
    success_url = reverse_lazy('contacts:list')

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'  # create this template
    success_url = reverse_lazy('contacts:list')


class ContactListListView(LoginRequiredMixin, ListView):
    model = ContactList
    template_name = "contacts/contactlist_list.html"
    context_object_name = "lists"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            ContactList.objects
            .select_related("owner")
            .annotate(member_count=Count("contacts", distinct=True))
            .order_by("name")
        )
        q = self.request.GET.get("q", "").strip()
        active = self.request.GET.get("active")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(owner__username__icontains=q)
            )
        if active in {"true", "false"}:
            qs = qs.filter(active=(active == "true"))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["active"] = self.request.GET.get("active", "")
        return ctx


class ContactListCreateView(LoginRequiredMixin, CreateView):
    model = ContactList
    form_class = ContactListForm
    template_name = "contacts/contactlist_create.html"
    success_url = reverse_lazy("contacts:contactlist_list")

    def form_valid(self, form):
        # Set owner on create
        obj = form.save(commit=False)
        if not obj.owner:
            obj.owner = self.request.user
        obj.save()
        form.save_m2m()
        messages.success(self.request, "Contact list created.")
        return super().form_valid(form)

class ContactListUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactList
    form_class = ContactListForm
    template_name = "contacts/contactlist_create.html"
    success_url = reverse_lazy("contacts:contactlist_list")

    def form_valid(self, form):
        messages.success(self.request, "Contact list updated.")
        return super().form_valid(form)
    model = ContactList
    form_class = ContactForm
    template_name = 'contacts/contactlist_update.html'  # reuse create template
    success_url = reverse_lazy('contacts:list')