OAuth2 and Lookup Utilities
===========================

This is the documentation for the :py:mod:`django-automationoauth` project which provides a pluggable Django
app with common utilities for authenticating requests by interacting with the LOOKUP and OAUTH services.

Installation and usage
----------------------

The modules can be installed from the git repo:

.. code:: bash

    $ pip install git+https://github.com/uisautomation/django-automationoauth

Add the following applications to ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        # ...
        'automationlookup',
        'automationoauth',
        # ...
    ]

.. note::

    If you use the ``automationlookup`` application, you *must* also add the
    ``automationoauth`` module to ``INSTALLED_APPS``.

OAuth2
------

.. automodule:: automationoauth

Token verification
``````````````````

.. automodule:: automationoauth.token
    :members:
    :member-order: bysource

Authenticating as an OAuth client
`````````````````````````````````

.. automodule:: automationoauth.client
    :members:
    :member-order: bysource

Settings
````````

.. automodule:: automationoauth.defaultsettings
    :members:
    :member-order: bysource

Lookup
------

.. automodule:: automationlookup
    :members:
    :member-order: bysource

Settings
````````

.. automodule:: automationlookup.defaultsettings
    :members:
    :member-order: bysource

Legacy API
``````````

The following API was imported directly from the first project ot make use of
our OAuth2 infrastructure and is deprecated.

'authentication' module
```````````````````````

.. automodule:: automationoauthdrf.authentication
    :members:

'lookup' module
```````````````

.. automodule:: automationlookup.lookup
    :members:

'models' module
```````````````

.. automodule:: automationlookup.models
    :members:

'oauth2client' module
`````````````````````

.. automodule:: automationoauthclient.__init__
    :members:
