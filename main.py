#!/usr/bin/env python
"""
The purpose of this module is to find all Pivotal stories tagged with 'sentry'
and report those stories 'accepted' on Pivotal but activate on Sentry.
"""
from pivotal_to_sentry.pivotal import PivotalClient


def main():
    pivotal = PivotalClient()
    project_id = pivotal.get_all_projects()[0]['id']
    stories = pivotal.get_all_stories(
        project_id, with_label='sentry', with_state='accepted'
    )
    for story in stories:
        print u'{}: {}'.format(story['id'], story['name'])


if __name__ == '__main__':
    main()
