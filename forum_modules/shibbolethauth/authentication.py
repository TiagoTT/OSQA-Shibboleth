from forum.authentication.base import AuthenticationConsumer, ConsumerTemplateContext, InvalidAuthentication

from forum.models import User
from forum.actions import UserJoinsAction
from django.contrib.auth import authenticate

import unicodedata

class ShibbolethAuthConsumer(AuthenticationConsumer):

    def process_authentication_request(self, request):

        # Check for the Shibboleth session header.
        if 'HTTP_SHIB_SESSION_ID' in request.META and request.META['HTTP_SHIB_SESSION_ID']:

            # Fetch the username and email from Shibboleth headers.
            utf8_username = request.META['HTTP_SSONAME'].decode('utf-8')
            # Create an ASCII compatible version of the username,
            # because OSQA/Django have bugs handling UTF8 strings in usernames.
            username = unicodedata.normalize('NFKD', utf8_username).encode('ascii', 'ignore')
            email = request.META['HTTP_SSOCONTACTMAIL']

            # Try to load the user from the database, by its email.
            user = None
            try:
                user = User.objects.get(email=email)
            except:
                pass

            if user is None:
                # The user was not found, so it must be a new user.
                # Let's create it on the database.
                user = User(username=username, email=email)
                user.email_isvalid = True
                user.set_unusable_password()
                user.save()
                UserJoinsAction(user=user, ip=request.META['REMOTE_ADDR']).save()

            # Return the User object of the authenticated user.
            return user

        else:
            raise InvalidAuthentication("Shibboleth Authentication Failure.")

