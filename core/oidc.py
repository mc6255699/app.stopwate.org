from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import Group
import jwt


ADMIN_GROUP_ID = '154b4b31-be89-46f3-94fe-cf8ce3caebc7'  # this is the id for Stopwaste_Django_Admin_Access


class AzureOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super().create_user(claims)
        user.username = claims.get('email', claims.get('preferred_username', user.username))
        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()
        self.set_user_groups(user, claims)
        return user
        
    def update_user(self, user, claims):
        user.username = claims.get('email', claims.get('preferred_username', user.username))
        user.email = claims.get('email', '')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()
        self.set_user_groups(user, claims)
        return user
    
    def set_user_groups(self, user, claims):
        groups = claims.get('groups', [])
        user.groups.clear()
        is_admin = False
        for group_id in groups:
            group_obj, _ = Group.objects.get_or_create(name=group_id)
            user.groups.add(group_obj)
            if group_id == ADMIN_GROUP_ID:
                is_admin = True
        user.is_staff = is_admin
        user.is_superuser = False  # Optional: or True if you want full access
        user.save()

#EXPOSES TOO MUCH _ DO NOT USE THIS ONE
def authenticate(self, request, **kwargs):
    print("🔍 AzureOIDCBackend.authenticate() called")
    result = super().authenticate(request, **kwargs)
    if result and request is not None:
        token_data = kwargs.get('response', {})
        if token_data:
            id_token = token_data.get('id_token')
            access_token = token_data.get('access_token')
            #print("🪪 ID Token:\n", id_token)
            #print("🔐 Access Token:\n", access_token)
            request.session['oidc_id_token'] = id_token
            request.session['oidc_access_token'] = access_token
            # Decode and store claims
            try:
                claims = jwt.decode(id_token, options={"verify_signature": False})
                request.session['oidc_id_token_claims'] = claims
            except Exception as e:
                request.session['oidc_id_token_claims'] = {"error": str(e)}

    return result

def authenticateREALs(self, request, **kwargs):
    print("🔍 AzureOIDCBackend.authenticate() called")
    result = super().authenticate(request, **kwargs)

    if result and request is not None:
        token_data = kwargs.get('response', {})
        if token_data:
            id_token = token_data.get('id_token')
            access_token = token_data.get('access_token')
            request.session['oidc_id_token'] = id_token
            request.session['oidc_access_token'] = access_token

            try:
                # Decode without verification for debug purposes
                claims = jwt.decode(id_token, options={"verify_signature": False})
                request.session['oidc_id_token_claims'] = claims
            except Exception as e:
                request.session['oidc_id_token_claims'] = {"error": str(e)}

    return result

