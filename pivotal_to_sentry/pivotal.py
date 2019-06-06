import os
from pivotal_to_sentry.rest import RestClient


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

    def paged_json_request(self, url, params=None, data=None, headers=None):
        params = params or {}
        offset = 0
        total = 1  # Prime the loop
        while offset < total:
            params['offset'] = offset
            response = self.request(url, params, data, headers)
            total = int(
                response.headers.get('x-tracker-pagination-total', '0')
            )
            offset = int(
                response.headers.get('x-tracker-pagination-offset', '0')
            )
            count = int(
                response.headers.get('x-tracker-pagination-returned', '0')
            )
            yield response.json()
            offset = offset + count

    def all_pages_json(self, url, params=None, data=None, headers=None):
        lst = []
        for page in self.paged_json_request(url, params, data, headers):
            lst += page
        return lst

    def get_projects(self):
        url = 'projects'
        response = self.request(url)
        return response.json()

    def get_stories(self, project_id, **filters):
        url = '/projects/{}/stories'.format(project_id)
        params = filters
        return self.all_pages_json(url, params=params)
