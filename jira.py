import getpass
import math
import os

import arrow
from arrow import Arrow
import requests as rest

import util


class Jira:
    def __init__(self):
        self.PAGE_SIZE = 50
        self.HOST = os.environ.get("JIRA_HOST") or input("Jira Host: ")
        assert self.HOST is not None, "You must specify a jira host!"
        self.URL = f"https://{self.HOST}"
        self.API_URL = self.URL + '/rest/api/2'
        self.USERNAME = os.environ.get("JIRA_USER") or input("Jira User: ")
        assert self.USERNAME is not None, "You must specify a jira user!"
        self.PASSWD = os.environ.get("JIRA_PASSWD") or getpass.getpass("Jira Password: ")
        self.AUTH = (self.USERNAME, self.PASSWD)

    def get_issues(self, jql: str) -> list[dict[str, any]]:
        util.debug_print(f'jql="{jql}"')
        search_params = {
            'jql': jql,
            'fields': ['summary', 'status', 'resolution']
        }
        data = self.get_all('/search', 'issues', search_params)

        issues = [{
            'key': i['key'],
            'summary': i['fields']['summary'],
            'resolution': util.get_field(i, 'fields', 'resolution', 'name'),
            'status': util.get_field(i, 'fields', 'status', 'name')
        } for i in data['issues']]
        return issues

    def attach_worklogs(self, issues, start: Arrow, end: Arrow = arrow.now()):
        for issue in issues:
            data = self.get_all(f"/issue/{issue['key']}/worklog", 'worklogs')
            worklogs = data['worklogs']

            issue['timeSpentSeconds'] = 0
            for record in worklogs:
                if util.get_field(record, 'author', 'name') == self.USERNAME:
                    time_started = arrow.get(record['started'])
                    if start < time_started < end:
                        issue['timeSpentSeconds'] = issue['timeSpentSeconds'] + record['timeSpentSeconds']

    def get_all(self, endpoint: str, what: str, params: dict[str, any] = None):
        if params is None:
            params = {}
        url = self.API_URL + endpoint
        data = rest.get(url, auth=self.AUTH, params=params).json()
        util.debug_print('OK GET', endpoint)
        if data['total'] > data['maxResults']:
            for page in range(1, math.ceil(data['total'] / self.PAGE_SIZE)):
                temp = rest.get(url, auth=self.AUTH, params={
                    **params,
                    'startAt': page * self.PAGE_SIZE
                }).json()
                util.debug_print('OK GET', endpoint)
                data[what] += temp[what]

        return data
