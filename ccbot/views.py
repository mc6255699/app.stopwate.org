import os
import subprocess
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CCRequestForm  # ✅ your new ModelForm
from dotenv import load_dotenv
from .models import CCRequest

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
    requests = CCRequest.objects.select_related('credit_card_name').order_by('-timestamp')
    return render(request, 'ccbot/cc_log.html', {'requests': requests})
