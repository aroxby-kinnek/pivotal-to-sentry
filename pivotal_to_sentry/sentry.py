import os
from pivotal_to_sentry.client import RestClient


class SentryClient(RestClient):
    base_url = 'https://sentry.io/api/0/'

    def _get_auth_token(self):
        token = os.environ.get('SENTRY_TOKEN')
        if not token:
            raise RuntimeError('SENTRY_TOKEN must be present')
        return token

    def __init__(self):
        self.auth_token = self._get_auth_token()

    def add_auth_data(self, params=None, data=None, headers=None):
        headers = headers or {}
        headers['Authorization'] = 'Bearer {}'.format(self.auth_token)
        return params, data, headers

    def request(self, url, params=None, data=None, headers=None):
        if not url.endswith('/'):
            url += '/'
        return super(SentryClient, self).request(url, params, data, headers)
