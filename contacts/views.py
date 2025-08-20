from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_GET,require_POST
from .models import *
from .forms import *
# contacts/views.py

# Create your views here.

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
    template_name = "contacts/contact_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'detail'
        context['form'] = ContactForm(instance=self.object)
        return context

#Using ths class as a function for creating a basic contact - It is straightforward and just uses the default crispyform. 
class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_add.html"
 
    def get_success_url(self):
        messages.success(self.request, "Contact created.")
        return reverse_lazy("contacts:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'create'
        return context
    
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_type'] = 'edit'
        return context
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
    template_name = "contacts/contactlist_edit.html"  # Or create.html if you wish
    success_url = reverse_lazy("contacts:contactlist_list")

    def form_valid(self, form):
        if not form.instance.owner_id:
            form.instance.owner = self.request.user
        messages.success(self.request, "Contact list created.")
        return super().form_valid(form)

class ContactListUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactList
    form_class = ContactListForm
    template_name = "contacts/contactlist_edit.html"  # Or update.html
    success_url = reverse_lazy("contacts:contactlist_list")

    def form_valid(self, form):
        messages.success(self.request, "Contact list updated.")
        return super().form_valid(form)


    #-----------------------AJAX VIEWS-----------------------




@login_required
@require_GET
def search_contact_by_name(request):
    q = (request.GET.get("q") or "").strip()
    exclude_for = request.GET.get("exclude_for")

    # Optional: avoid super-short searches
    if len(q) < 2:
        return JsonResponse({"results": []})

    qs = Contact.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )

    if exclude_for and exclude_for.isdigit():
        qs = qs.exclude(pk=int(exclude_for))  # exclude the specific contact id

    results = list(
        qs.order_by("first_name", "last_name")
          .values("id", "first_name", "last_name")[:10]
    )

    return JsonResponse({"results": results})

@login_required
def search_contact_lists(request):
    """
    GET /contacts/lists/search/?q=ma&exclude_for=12
    Returns up to 10 active lists matching 'q', excluding lists the contact already belongs to.
    """
    q = (request.GET.get("q") or "").strip()
    exclude_for = request.GET.get("exclude_for")

#    qs = ContactList.objects.filter(active=True)
    qs = ContactList.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    if exclude_for and exclude_for.isdigit():
        qs = qs.exclude(contacts__id=int(exclude_for))

    results = list(qs.order_by("name")[:10].values("id", "name"))
    return JsonResponse({"results": results})

@login_required
def add_contact_to_list(request, pk=None, contact_id=None):
    """
    POST list_id -> add membership
    Handles URLs with either pk or contact_id parameter
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    # Use either pk or contact_id parameter
    contact_pk = contact_id if contact_id is not None else pk
    contact = get_object_or_404(Contact, pk=contact_pk)

    list_id = request.POST.get("list_id")
    if not list_id:
        return HttpResponseBadRequest("list_id required")

    cl = get_object_or_404(ContactList, pk=list_id)
    cl.contacts.add(contact)  # M2M is on ContactList.contacts

    # Redirect back to the contact edit page after successful addition
    messages.success(request, f"Contact added to list: {cl.name}")
    return redirect('contacts:update', pk=contact.pk)

@login_required
def remove_contact_from_list(request, pk):
    """
    POST list_id -> remove membership
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    contact = get_object_or_404(Contact, pk=pk)
    list_id = request.POST.get("list_id")
    if not list_id:
        return HttpResponseBadRequest("list_id required")

    cl = get_object_or_404(ContactList, pk=list_id)
    cl.contacts.remove(contact)
    messages.success(request, f"removed from list : {cl.name}")
    return redirect('contacts:update', pk=contact.pk)
#    return JsonResponse({"ok": True})



@login_required
def add_sublist_to_list(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    mainlist = get_object_or_404(ContactList, pk=pk)
    sublist_id = request.POST.get("sublist_id")
    if not sublist_id:
        return HttpResponseBadRequest("sublist_id required")
    sublist = get_object_or_404(ContactList, pk=sublist_id)
    mainlist.sublists.add(sublist)
    return JsonResponse({"ok": True})

@login_required
def remove_sublist_from_list(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    mainlist = get_object_or_404(ContactList, pk=pk)
    sublist_id = request.POST.get("sublist_id")
    if not sublist_id:
        return HttpResponseBadRequest("sublist_id required")
    sublist = get_object_or_404(ContactList, pk=sublist_id)
    mainlist.sublists.remove(sublist)
    return JsonResponse({"ok": True})


#used to get contact data as json to return to the dynamic contact add function 
def contact_detail_api(request, pk):
    c = get_object_or_404(Contact, pk=pk)
    return JsonResponse({
        "id": c.id,
        "first_name": c.first_name or "",
        "last_name": c.last_name or "",
        "job_title": c.job_title or "",
        "organization": c.organization or "",
        "email": c.email or "",
        "phone_number": c.phone_number or "",
    })

@require_POST
@login_required
def contactlist_remove_contact(request, pk, contact_id):
    cl = get_object_or_404(ContactList, pk=pk)
    contact = get_object_or_404(Contact, pk=contact_id)
    cl.contacts.remove(contact)
    messages.success(request, f"Removed {contact.first_name} {contact.last_name} from “{cl.name}”.")
    return redirect("contacts:contactlist_edit", pk=pk)

@login_required
def contact_search_ajax(request):
    """
    Return JSON list of contacts matching a search query.
    Excludes contacts already in the list if `list_id` is provided.
    """
    query = request.GET.get("q", "").strip()
    list_id = request.GET.get("list_id")

    if not query:
        return JsonResponse([], safe=False)

    qs = Contact.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
    )

    # Exclude contacts already in list
    if list_id:
        try:
            clist = ContactList.objects.get(pk=list_id)
            qs = qs.exclude(pk__in=clist.contacts.values_list("pk", flat=True))
        except ContactList.DoesNotExist:
            pass

    results = [
        {"id": c.id, "first_name": c.first_name, "last_name": c.last_name, "email": c.email or ""}
        for c in qs[:20]  # limit results to 20
    ]

    return JsonResponse(results, safe=False)

@login_required
@require_POST
def contactlist_add_contact(request, list_id, contact_id):
    contact_list = get_object_or_404(ContactList, pk=list_id)
    contact = get_object_or_404(Contact, pk=contact_id)

    if contact not in contact_list.contacts.all():
        contact_list.contacts.add(contact)
        messages.success(request, f"{contact.first_name} {contact.last_name} added to the list.")
    else:
        messages.info(request, f"{contact.first_name} {contact.last_name} is already in the list.")

    return redirect("contacts:contactlist_edit", pk=list_id)

#round 2 of ajax add functions. 

def contact_add(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contacts:list")
    else:
        form = ContactForm()
    return render(request, "contacts/contact_form.html", {"form": form, "mode": "add"})

def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("contacts:detail", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_form.html", {"form": form, "object": contact, "mode": "edit"})

def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "contacts/contact_form.html", {"object": contact, "mode": "detail"})

def search_contact_lists(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        lists = ContactList.objects.filter(name__icontains=query).order_by("name")[:10]
        results = [{"id": cl.id, "name": cl.name} for cl in lists]
    return JsonResponse({"results": results})

@require_POST
def contactlist_add_contact(request, list_id, contact_id):
    contact_list = get_object_or_404(ContactList, pk=list_id)
    contact = get_object_or_404(Contact, pk=contact_id)
    contact_list.contacts.add(contact)
    return JsonResponse({"status": "success", "list_id": list_id, "contact_id": contact_id})
