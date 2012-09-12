# OSQA Shibboleth Authentication Module


## Description

All this work was done as part of my job at [SAPO](http://www.sapo.pt/).  
This is how I did it.


### Starting point

OSQA code base starting point was fantasy-island-0.9.0-beta3 obtained from the official site.
* http://www.osqa.net/
* http://www.osqa.net/releases/fantasy-island-0.9.0-beta3.tar.gz


### Authentication module

This is how I started:

1. I read the other authentication modules, found in:  
    `forum_modules/`

2. I read the authentication process code, found in:  
    `forum/views/auth.py`

3. I have added a directory for this new module and placed an empty init file:  
    `forum_modules/shibbolethauth/`  
    `forum_modules/shibbolethauth/__init__.py`

4. Then I coded the authentication module itself in:  
    `forum_modules/shibbolethauth/authentication.py`

This is how the module operates:

1. The module checks for the Shibboleth session ID variable, and proceeds if it is present.

2. The username and email are then retrieved from the respective Shibboleth session variables.

3. The module tries to load the user, by its email. If the user is found it is returned.

4. If the user was not found, it is created and then returned.

5. The user returned will be considered valid and authenticated by OSQA and a new session will be created for it.

### Login URL change

I didn't make the authentication transparent. The user still has to click the "login" link to authenticate, but instead of loading to the login form URL, the Shibboleth authentication module URL is loaded. Then the authentication module checks the HTTP Shibboleth session headers and a new session is created.  

The login URL was changed in file:  
    `forum/urls.py`

I looked for `account/signin` and found the line:  
    `url(r'^%s%s$' % (_('account/'), _('signin/')), app.auth.signin_page, name='auth_signin'),`

Which I replaced with:  
```
url(r'^%s%s$' % (_('account/'), _('signin/')),
  'django.views.generic.simple.redirect_to',
  {'url': '/account/shibboleth/signin'},
  name='auth_signin'),
```


## Install and use


### Prerequisites

It is assumed that you already have:
* an OSQA instance installed and running
* the Shibboleth authentication system working
* a web server (or reverse proxy) with the Shibboleth module active and protecting the OSQA instance URL


### Put the module in place

Place the module inside the application root directory:  
    `cd osqa_root_dir`  
    `cp -r /tmp/osqa-shibboleth/forum_modules/shibbolethauth/ forum_modules/`

### Adjust the names of the Shibboleth HTTP header variables

In my case these were the names of the relevant Shibboleth variables:
* `HTTP_SHIB_SESSION_ID` - the Shibboleth session ID, which indicates that there is a valid user
* `HTTP_SSONAME` - the user's full name
* `HTTP_SSOCONTACTMAIL` - the user's email address

Most likely, you will need to edit the code in order to adjust these.  
    `vim forum_modules/shibbolethauth/authentication.py`

### Adjust login URL

If you are using exactly the same OSQA release I did, you can just copy my version of this file:  
    `cp /tmp/osqa-shibboleth/forum/urls.py forum/urls.py`

Otherwise, perform the steps described in "Login URL change" manually:  
    `vim forum/urls.py`

# Good luck!
