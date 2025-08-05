
import urllib
import requests
import jwt
import pprint
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as django_logout

from urllib.parse import urlencode
from urllib.parse import quote
from urllib.parse import unquote


#from mozilla_django_oidc.auth import OIDCAuthenticationBackend
#from mozilla_django_oidc.views import OIDCAuthenticationCallbackView, OIDCAuthenticationRequestView
#from mozilla_django_oidc.views import OIDCAuthenticationRequestView





##HELPER FUNCTIONS FOR OIDC LOGIN AND CALLBACK
def dump_full_request(request):
    pprint.pprint({
        "method": request.method,
        "url": request.build_absolute_uri(),
        "headers": dict(request.headers),
        "GET": request.GET.dict(),
        "POST": request.POST.dict(),
    })




def full_logout(request):
    if request.method != "POST":
        return redirect("/")  # or 405 if you want stricter

    django_logout(request)
    tenant = os.getenv("OIDC_TENANT_ID")  # ensure this is set
    post_logout = request.build_absolute_uri("/")  # where user returns after Azure logout
    params = {"post_logout_redirect_uri": post_logout}
    logout_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout?{urlencode(params)}"
    return redirect(logout_url)




# def oidc_login(request):
#     tenant_id = settings.OIDC_TENANT_ID
#     client_id = settings.OIDC_RP_CLIENT_ID
#     redirect_uri = request.build_absolute_uri('/oidc/callback/')
#     next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)


#     base_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
#     params = {
#         "client_id": client_id,
#         "response_type": "code",
#         "redirect_uri": redirect_uri,
#         "response_mode": "query",
#         "scope": "openid profile email",
        
#     }
#     if settings.DEBUG:
#         params["prompt"] = "login"  # Force login during development
#     login_url = f"{base_url}?{urllib.parse.urlencode(params)}"
#     return redirect(login_url)

# def logged_out(request):
#     return render(request, 'core/logged_out.html')  # Make sure your template is in core/templates/core/

# def oidc_logout(request):
#     logout(request)  # Clear Django session
#     base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
#     post_logout_redirect_uri = request.build_absolute_uri("/core/logged-out/")
#     params = urlencode({'post_logout_redirect_uri': post_logout_redirect_uri})
#     return redirect(f"{base_url}?{params}")



@login_required
def hub(request):
    return render(request, 'core/hub.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('core:hub')  # Redirect to hub if user is authenticated
    else:
        return render(request, 'core/home.html')  # Render home page for unauthenticated users
    
@login_required
def dashboard(request):
    user = request.user
    id_token = request.session.get('oidc_id_token', '')
    claims = {}

    # Decode the ID token to get claims if not already present
    if id_token:
        try:
            # Decode without verification (since we just want claims)
            claims = jwt.decode(id_token, options={"verify_signature": False, "verify_aud": False})
        except Exception as e:
            claims = {"error": str(e)}

    context = {
        'user': user,
        'claims': claims,
        'id_token': id_token,
    }
    return render(request, 'core/dashboard.html', context)

def user_debug(request):
    user = request.user
    id_token = request.session.get('oidc_id_token', '')
    claims = {}

    # Decode the ID token to get claims if not already present
    if id_token:
        try:
            # Decode without verification (since we just want claims)
            claims = jwt.decode(id_token, options={"verify_signature": False, "verify_aud": False})
        except Exception as e:
            claims = {"error": str(e)}

    group_ids = claims.get('groups', [])
    group_names = []

    access_token = request.session.get('oidc_access_token')
    if access_token and group_ids:
        # Batch request for efficiency (max 20 per batch)
        batch = []
        for group_id in group_ids:
            batch.append({
                "id": group_id,
                "method": "GET",
                "url": f"/groups/{group_id}"
            })
        batch_request = {"requests": batch}
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(
            "https://graph.microsoft.com/v1.0/$batch",
            json=batch_request,
            headers=headers
        )
        if resp.status_code == 200:
            results = resp.json().get("responses", [])
            for result in results:
                if result.get("status") == 200:
                    group_names.append(result["body"].get("displayName", result["id"]))
                else:
                    group_names.append(result["id"])
        else:
            # fallback: just show IDs
            group_names = group_ids

    context = {
        'user': user,
        'claims': claims,
        'id_token': id_token,
        'group_names': group_names,
    }
    return render(request, 'core/user_debug.html', context)




