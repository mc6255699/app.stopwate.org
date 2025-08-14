import os
import subprocess
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CCRequestForm  # ✅ your new ModelForm
from dotenv import load_dotenv
from .models import CCRequest
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
import csv



load_dotenv()  # Load OP_SERVICE_ACCOUNT_TOKEN, CC_VAULT_ID

@login_required
def request_card(request):
    if request.method == 'POST':
        form = CCRequestForm(request.POST)
        if form.is_valid():
            user = request.user
            user_email = user.email
            user_full_name = f"{user.first_name} {user.last_name}"

            # Create model instance but don't save yet
            cc_request = form.save(commit=False)
            cc_request.requested_by = user_email  # ✅ set requested_by
            cc_request.save()  # ✅ save to DB

            # Get related info from saved instance
            description = cc_request.description
            amount = cc_request.amount
            vendor = cc_request.vendor
            cc_recipient_obj = cc_request.credit_card_name
            cc_recipient_id = cc_recipient_obj.onepassword_id  # ✅ get 1Password ID

            # Load env vars
            token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
            vault_id = os.getenv("CC_VAULT_ID")
            item_id = cc_recipient_id  # used in CLI call

            if not all([token, vault_id, item_id]):
                return render(request, 'ccbot/form.html', {
                    'form': form,
                    'error': "Missing environment configuration."
                })

            os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = token

            try:
                result = subprocess.run(
                    ["op", "item", "share", item_id,
                     "--vault", vault_id,
                     "--emails", user_email,
                     "--expires-in", "24h"],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                share_link = result.stdout.strip()
            except subprocess.CalledProcessError as e:
                return render(request, 'ccbot/form.html', {
                    'form': form,
                    'error': f"Failed to generate 1Password link: {e.stderr}"
                })

            # Send email
            send_mail(
                subject="Your Secure Credit Card Link",
                message=(
                    f"Hello {user_full_name},\n\n"
                    f"You requested access to a shared credit card.\n\n"
                    f"Vendor: {vendor}\n"
                    f"Description: {description}\n"
                    f"Amount: ${amount}\n\n"
                    f"Secure Link: {share_link}\n\n"
                    f"This link will expire in 24 hours."
                ),
                from_email="donotreply@stopwaste.org",
                recipient_list=[user_email],
                fail_silently=False
            )

            return render(request, 'ccbot/success.html', {
                "user_full_name": user_full_name,
                #"user_email": user_email,
                "user_email": "mcohen@stopwaste.org",
                
                "cc_recipient_id": cc_recipient_id,
                "description": description,
                "amount": amount,
                "vendor": vendor,
                "share_link": share_link,
            })

        # Invalid form
        return render(request, 'ccbot/form.html', {'form': form})

    # GET request
    form = CCRequestForm()
    return render(request, 'ccbot/form.html', {'form': form})

from .models import CCRequest

@login_required
def cc_log(request):
    requests_qs = _filter_cc_requests(request)
    card_names = (
        CCRequest.objects.select_related("credit_card_name")
        .values_list("credit_card_name__cc_name", flat=True)
        .distinct()
        .order_by("credit_card_name__cc_name")
    )
    return render(request, "ccbot/cc_log.html", {
        "requests": requests_qs,
        "card_names": card_names,
    })

def _filter_cc_requests(request):
    qs = CCRequest.objects.select_related("credit_card_name").order_by("-timestamp")
    q = (request.GET.get("q") or "").strip()
    date_from = (request.GET.get("date_from") or "").strip()
    date_to = (request.GET.get("date_to") or "").strip()
    min_amt = (request.GET.get("min_amount") or "").strip()
    max_amt = (request.GET.get("max_amount") or "").strip()
    card = (request.GET.get("card") or "").strip()

    if q:
        qs = qs.filter(
            Q(vendor__icontains=q) |
            Q(description__icontains=q) |
            Q(requested_by__icontains=q)
        )
    if date_from:
        qs = qs.filter(timestamp__date__gte=date_from)
    if date_to:
        qs = qs.filter(timestamp__date__lte=date_to)
    if min_amt:
        try: qs = qs.filter(amount__gte=float(min_amt))
        except ValueError: pass
    if max_amt:
        try: qs = qs.filter(amount__lte=float(max_amt))
        except ValueError: pass
    if card:
        qs = qs.filter(credit_card_name__cc_name__iexact=card)

    return qs

def cc_requests_export_csv(request):
    rows = _filter_cc_requests(request)

    # Include today's local date in the filename
    today_str = timezone.localdate().strftime("%Y-%m-%d")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="cc_requests_{today_str}.csv"'

    writer = csv.writer(response)
    # No Payment Code column
    writer.writerow(["Date (MM/DD/YY)", "Requested By", "Vendor", "Description", "Amount", "Card"])

    for r in rows:
        local_date = timezone.localtime(r.timestamp).strftime("%m/%d/%y") if r.timestamp else ""
        requested_by = str(r.requested_by) if r.requested_by is not None else ""
        vendor = r.vendor or ""
        description = r.description or ""
        # USD formatting with comma separators + 2 decimals
        amount_str = f"${r.amount:,.2f}" if r.amount is not None else ""
        card_name = getattr(r.credit_card_name, "cc_name", "") or ""

        writer.writerow([local_date, requested_by, vendor, description, amount_str, card_name])

    return response