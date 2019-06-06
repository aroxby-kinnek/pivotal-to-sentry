import os
import re
from pivotal_to_sentry.rest import RestClient


class SentryClient(RestClient):
    base_url = 'https://sentry.io/api/0/'

    class PageLink(object):
        def __init__(self, link, rel, results, cursor):
            self.link = link
            self.rel = rel
            self.results = results.lower() == 'true'
            self.cursor = cursor

        @classmethod
        def parse_link_header(cls, header):
            regex = (
                '^'
                r'<(?P<link>[^>]+)>'
                r';\s*rel="(?P<rel>[^"]+)"'
                r';\s*results="(?P<results>[^"]+)"'
                r';\s*cursor="(?P<cursor>[^"]+)"'
                '$'
            )
            links = [
                part.strip() for part in header.split(',') if part.strip()
            ]
            cursors = []
            while links:
                link = links[0]
                links = links[1:]
                match = re.match(regex, link)
                if not match:
                    raise ValueError('Malformed link header')
                cursor = cls(**match.groupdict())
                cursors.append(cursor)
            return cursors

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

    def paged_json_request(self, url, params=None, data=None, headers=None):
        while url:
            response = self.request(url, params, data, headers)
            link_header = response.headers.get('Link', '')
            links = self.PageLink.parse_link_header(link_header)
            named_links = {
                link.rel: link.link for link in links if link.results
            }
            url = named_links.get('next')
            if url:  # Bit of a hack
                url = url.replace(self.base_url, '')
            yield response.json()

    def all_pages_json(self, url, params=None, data=None, headers=None):
        lst = []
        for page in self.paged_json_request(url, params, data, headers):
            lst += page
        return lst

    def get_projects(self):
        url = 'projects/'
        return self.all_pages_json(url)

    def get_issues(self, organization, project):
        url = 'projects/{}/{}/issues/'.format(organization, project)
        return self.all_pages_json(url)
