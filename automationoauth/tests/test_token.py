"""
Test token verification

"""
import datetime
import json
from unittest import mock
from django.http import HttpRequest
from django.test import TestCase
from requests import Response
from rest_framework.request import Request
from automationoauth.token import verify_token, InvalidTokenError


class InvalidTokenErrorTest(TestCase):
    def test_reason(self):
        """Passing a reason works."""
        e = InvalidTokenError('some reason')
        self.assertEqual(e.reason, 'some reason')

    def test_no_reason(self):
        """Passing no reason works."""
        e = InvalidTokenError()
        self.assertEqual(e.reason, '')


class VerificationTest(TestCase):
    GOOD_TOKEN = 'GOOD_TOKEN'
    UNKNOWN_TOKEN = 'UNKNOWN_TOKEN'
    FUTURE_TOKEN = 'FUTURE_TOKEN'
    PAST_TOKEN = 'PAST_TOKEN'
    NO_SUBJECT_TOKEN = 'NO_SUBJECT_TOKEN'

    def setUp(self):
        # Create an empty HTTP request
        self.request = Request(HttpRequest())

    def test_good_token(self):
        """A request with a good token is authenticated."""
        with self.patch_oauth2_session():
            result = verify_token(VerificationTest.GOOD_TOKEN)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_empty_subject(self):
        """An otherwise good token with no subject is still good."""
        with self.patch_oauth2_session():
            result = verify_token(VerificationTest.NO_SUBJECT_TOKEN)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    def test_unknown_token(self):
        """A completely unknown token is invalid."""
        with self.patch_oauth2_session(), self.assertRaises(InvalidTokenError):
            verify_token(VerificationTest.UNKNOWN_TOKEN)

    def test_past_token(self):
        """A token from the past is invalid."""
        with self.patch_oauth2_session(), self.assertRaises(InvalidTokenError):
            verify_token(VerificationTest.PAST_TOKEN)

    def test_future_token(self):
        """A token from the future is invalid."""
        with self.patch_oauth2_session(), self.assertRaises(InvalidTokenError):
            verify_token(VerificationTest.FUTURE_TOKEN)

    def patch_oauth2_session(self):
        """Patch the internal request session used by the authenticator."""
        mock_request = mock.MagicMock()

        def side_effect(*args, **kwargs):
            token = kwargs.get('data', {}).get('token')

            # By default, the response is success with inactive token
            response = Response()
            response.status_code = 200
            response._content = json.dumps(dict(active=False)).encode('utf8')

            if token == VerificationTest.GOOD_TOKEN:
                response._content = json.dumps(dict(
                    sub='testing:test0001',
                    active=True, iat=_utc_now() - 1000, exp=_utc_now() + 1000)).encode('utf8')
            elif token == VerificationTest.FUTURE_TOKEN:
                response._content = json.dumps(dict(
                    sub='testing:test0001',
                    active=True, iat=_utc_now() + 1000, exp=_utc_now() + 3000)).encode('utf8')
            elif token == VerificationTest.PAST_TOKEN:
                response._content = json.dumps(dict(
                    sub='testing:test0001',
                    active=True, iat=_utc_now() - 3000, exp=_utc_now() - 1000)).encode('utf8')
            elif token == VerificationTest.NO_SUBJECT_TOKEN:
                response._content = json.dumps(dict(
                    active=True, iat=_utc_now() - 1000, exp=_utc_now() + 1000)).encode('utf8')
            elif token == VerificationTest.UNKNOWN_TOKEN:
                pass  # default response suffices
            else:
                assert False, "Unexpected token value: {}".format(repr(token))

            return response

        mock_request.side_effect = side_effect

        # Mock OAuth2Session to return our session mock
        mock_get_session = mock.MagicMock()
        mock_get_session.return_value.request = mock_request

        return mock.patch('automationoauth.client.OAuth2Session', mock_get_session)


def _utc_now():
    """Return a UNIX-style timestamp representing "now" in UTC."""
    return (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
