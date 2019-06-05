import requests
from pivotal_to_sentry.exceptions import RestAPIException


class RestClient(object):
    def add_auth_data(self, params=None, data=None, headers=None):
        raise NotImplementedError

    @property
    def base_url(self):
        raise NotImplementedError

    def _raise_for_response(self, response):
        try:
            content = response.json()
        except ValueError:
            content = response.content
        if content == '':
            content = '[empty response]'
        message = 'HTTP {}:\n{}'.format(response.status_code, content)
        raise RestAPIException(message)

    def request(self, url, params=None, data=None, headers=None):
        url = self.base_url + url
        params, data, headers = self.add_auth_data(params, data, headers)
        response = requests.get(
            url=url, params=params, data=data, headers=headers
        )
        if response.status_code / 100 != 2:
            self._raise_for_response(response)
        return response

    def json_request(self, url, params=None, data=None, headers=None):
        resp = self.request(url, params=params, data=data)
        return resp.json()
