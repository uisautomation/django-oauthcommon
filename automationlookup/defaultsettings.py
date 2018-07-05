"""
Default settings values for the :py:mod:`automationlookup` application.

"""
# Variables whose names are in upper case and do not start with an underscore from this module are
# used as default settings for the automationlookup application. See AutomationLookupConfig in
# .apps for how this is achieved. This is a bit mucky but, at the moment, Django does not have a
# standard way to specify default values for settings.  See:
# https://stackoverflow.com/questions/8428556/

LOOKUP_ROOT = 'https://lookupproxy.automation.uis.cam.ac.uk/'
"""
Root of lookup proxy API.

"""

LOOKUP_RESPONSE_CACHE_LIFETIME = 30
"""
Lifetime of the cached lookup response in seconds.

"""

LOOKUP_OAUTH2_SCOPES = ['lookup:anonymous']
"""
OAuth2 scopes which are required to access the lookupproxy API.

"""
