#!/usr/bin/env python
"""
The purpose of this module is to find all unresolved Sentry issues which
are linked to a resolved pivotal story
"""
from pivotal_to_sentry.pivotal import PivotalClient
from pivotal_to_sentry.sentry import (
    SentryClient,
    annotation_to_pivotal_story,
    url_for_issue,
)


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
    return linked, org_slug


def filter_pivotal_stories(stories, **filters):
    pivotal = PivotalClient()
    project_id = pivotal.get_projects()[0]['id']
    filtered = []
    for story_id in stories:
        story = pivotal.get_story(project_id, story_id)
        results = [story[key] == val for key, val in filters.iteritems()]
        if all(results):
            filtered.append(story_id)
    return filtered


def main():
    issues, org_slug = get_sentry_issues_with_pivotal()
    stories = {
        story for stories in issues.values() for story in stories
    }
    stories = filter_pivotal_stories(stories, current_state='accepted')
    # Drop unaccepted stories
    for issue_id in issues.keys():
        issues[issue_id] = [
            story for story in issues[issue_id] if story in stories
        ]
    # Drop issues with no stories
    issues = {k: v for k, v in issues.iteritems() if v}

    print 'Stories to resolve:'
    for issue in issues:
        url = url_for_issue(org_slug, issue)
        print url


if __name__ == '__main__':
    main()
