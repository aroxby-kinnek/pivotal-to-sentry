import os
from pivotal_to_sentry.client import RestClient


class PivotalClient(RestClient):
    base_url = 'https://www.pivotaltracker.com/services/v5/'

    def _get_auth_token(self):
        token = os.environ.get('PIVOTAL_TRACKER_TOKEN')
        if not token:
            raise RuntimeError('PIVOTAL_TRACKER_TOKEN must be present')
        return token

    def __init__(self):
        self.auth_token = self._get_auth_token()

    def add_auth_data(self, params=None, data=None, headers=None):
        headers = headers or {}
        headers['X-TrackerToken'] = self.auth_token
        return params, data, headers
