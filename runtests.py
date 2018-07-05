import django
import sys
from django.conf import settings
from django.test.runner import DiscoverRunner

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'automationlookup',
        'automationoauth',
    ),
    OAUTH2_INTROSPECT_URL='http://oauth2.example.com/oauth2/introspect',
    OAUTH2_TOKEN_URL='http://oauth2.example.com/oauth2/token',
    OAUTH2_CLIENT_ID='api-client-id',
    OAUTH2_CLIENT_SECRET='api-client-secret',
    OAUTH2_MAX_RETRIES=5,
    LOOKUP_ROOT='http://lookupproxy.invalid/',
    LOOKUP_PEOPLE_CACHE_LIFETIME=1800,
)

# Django >= 1.8
django.setup()
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(
    ['automationlookup', 'automationoauthclient', 'automationoauthdrf',
     'automationoauth']
)
if failures:
    sys.exit(failures)
