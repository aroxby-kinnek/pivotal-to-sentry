#!/usr/bin/env python
"""
The purpose of this module is to find all unresolved Sentry issues which
are linked to a resolved pivotal story
"""
from pivotal_to_sentry.pivotal import PivotalClient
from pivotal_to_sentry.sentry import SentryClient


def show_accepted_pivotal_stories():
    pivotal = PivotalClient()
    project_id = pivotal.get_projects()[0]['id']
    stories = pivotal.get_stories(
        project_id, with_label='sentry', with_state='accepted'
    )
    for story in stories:
        print u'{}: {}'.format(story['id'], story['name'])


def show_linked_sentry_events():
    sentry = SentryClient()
    projects = sentry.get_projects()
    proejcts_by_name = {project['name']: project for project in projects}
    project = proejcts_by_name['Kinnek Django']
    org_slug = project['organization']['slug']
    proj_slug = project['slug']

    # It's a pitty we can't filter for 'annotations' in the API
    issues = sentry.get_issues(org_slug, proj_slug, query='is:unresolved')
    issues = [issue for issue in issues if issue.get('annotations')]
    print len(issues)


def main():
    show_linked_sentry_events()


if __name__ == '__main__':
    main()
