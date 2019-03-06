# django-automationoauth

> This repository has moved to **https://gitlab.developers.cam.ac.uk/uis/devops/django/automationoauth**

[![Build Status](https://travis-ci.org/uisautomation/django-automationoauth.svg?branch=master)](https://travis-ci.org/uisautomation/django-automationoauth)
[![Build Status](https://codecov.io/gh/uisautomation/django-automationoauth/branch/master/graph/badge.svg)](https://codecov.io/gh/uisautomation/django-automationoauth)

The pluggable Django app provide a common utilities for authenticating requests
by interacting with the LOOKUP and OAUTH services.

Generated documentation can be found at https://uisautomation.github.io/django-automationoauth.

## Getting Started

To create a virtual environment (a one-off command):

```
virtualenv -p python3.6 venv
```

To activate the virtual environment (run for every new session):

```
source venv/bin/activate
```

To install the requirements from the setup.py (a one-off command):

```
pip install -e .
```

## Running the test suite

The [tox](https://tox.readthedocs.io/) automation tool is used to run tests
inside their own virtualenv. This way we can be sure that we know which packages
are required to run the tests. By default tests are run in a sqlite database
within a per-environment temporary directory. Other databases can be used by
setting the **DJANGO_DB_...** environment variables.

To run the test suite:

```
tox
```

## Generating database migrations

The ``tox`` environment "makemigrations" can be used like the "makemigrations"
management command:

```bash
$ tox -e makemigrations [-n NAME] <appname>
```

## Configuration

The app's utilities variously require the following Django settings to
be defined within the including project.

| Setting | Description |
| ------- | ----------- |
| OAUTH2_INTROSPECT_SCOPES | List of OAuth2 scopes the API server will request for the token it will use with the token introspection endpoint. |
| OAUTH2_INTROSPECT_URL | URL of the OAuth2 token introspection endpoint. The API server will first identify itself to the OAuth2 token endpoint and request an access token for this endpoint. |
| OAUTH2_TOKEN_URL | URL of the OAuth2 token endpoint the API server uses to request an authorisation token to perform OAuth2 token introspection. |
| OAUTH2_CLIENT_ID | OAuth2 client id which the API server uses to identify itself to the OAuth2 token introspection endpoint. |
| OAUTH2_CLIENT_SECRET | OAuth2 client secret which the API server uses to identify itself to the OAuth2 token introspection endpoint. |
| OAUTH2_TOKEN_URL | URL of the OAuth2 token endpoint the API server uses to request an authorisation token to perform OAuth2 token introspection. |
| OAUTH2_INTROSPECT_URL | URL of the OAuth2 token introspection endpoint. The API server will first identify itself to the OAuth2 token endpoint and request an access token for this endpoint. |
| OAUTH2_INTROSPECT_SCOPES | List of OAuth2 scopes the API server will request for the token it will use with the token introspection endpoint. |
| OAUTH2_LOOKUP_SCOPES | List of OAuth2 scopes the API server will request for the token it will use with lookup. |
| OAUTH2_MAX_RETRIES | Maximum number of retries when fetching URLs from the OAuth2 endpoint or OAuth2 authenticated URLs. This applies only to failed DNS lookups, socket connections and connection timeouts, never to requests where data has made it to the server. |
| LOOKUP_OAUTH2_SCOPES | List of OAuth2 scopes the API server will request for the token it will use with lookup. |
| LOOKUP_ROOT | URL of the lookup proxy's API root. |
| LOOKUP_PEOPLE_CACHE_LIFETIME | Responses to the people endpoint of lookupproxy are cached to increase performance. We assume that lookup details on people change rarely. This setting specifies the lifetime of a single cached lookup resource for a person in seconds. |
