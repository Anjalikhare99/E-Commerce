from .models import User
from social_core.exceptions import AuthException
from django.contrib.auth import logout

def get_or_create_user_by_email(strategy, details, backend, uid, user=None, *args, **kwargs):
    print("Custom pipeline called with email:", details.get('email'))

    email = details.get('email')
    if not email:
        raise AuthException(backend, 'Email is required to login.')

    if user:
        if user.email == email:
            print("User already exists with matching email:", user)
            return {'user': user}
        else:
            print("Email mismatch! Logged in user:", user.email, "Google email:", email)

            request = strategy.request
            logout(request)
            return {'user': None}

    try:
        user = User.objects.get(email=email)
        print("User found by email:", user)
    except User.DoesNotExist:
        username = email.split('@')[0]
        user = User.objects.create_user(username=username, email=email)
        user.save()
        print("New user created:", user)

    return {'user': user}


def prevent_auto_associate_by_uid(backend, uid, user=None, *args, **kwargs):
    """
    Prevent associating a social account (uid) with an existing user
    unless it's explicitly matched.
    """
    if user:
        return {'user': user}

    # If no user, try to find existing social auth
    social = backend.strategy.storage.user.get_social_auth(backend.name, uid)
    if social:
        return {'user': social.user}

    return {'user': None}

