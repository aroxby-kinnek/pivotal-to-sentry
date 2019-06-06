#!/usr/bin/env python
"""
The purpose of this module is to find all unresolved Sentry issues which
are linked to a resolved pivotal story
"""
from pivotal_to_sentry.pivotal import PivotalClient
from pivotal_to_sentry.sentry import SentryClient, annotation_to_pivotal_story


def get_sentry_issues_with_pivotal():
    sentry = SentryClient()
    projects = sentry.get_projects()
    proejcts_by_name = {project['name']: project for project in projects}
    project = proejcts_by_name['Kinnek Django']
    org_slug = project['organization']['slug']
    proj_slug = project['slug']

    issues = sentry.get_issues(org_slug, proj_slug, query='is:unresolved')
    # It's a pitty we can't filter for 'annotations' in the API
    issues = [issue for issue in issues if issue.get('annotations')]

    linked = {
        issue['id']: [
            annotation_to_pivotal_story(tag) for tag in issue['annotations']
        ] for issue in issues
    }
    return linked


def main():
    get_sentry_issues_with_pivotal()


if __name__ == '__main__':
    main()
