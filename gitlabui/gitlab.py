from requests import request
import re
import os
import json


class GitlabApi:
    def __init__(self, url, token, logger=None):
        self.url = url
        self.token = token
        self.logger = logger
        self.db = './projects.json'

    def request(self, method, path, **kwargs):
        return request(method, self.url + path, headers={'PRIVATE-TOKEN': self.token}, **kwargs)

    def get(self, path, **kwargs):
        return self.request('get', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('post', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('put', path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request('patch', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('delete', path, **kwargs)

    def get_projects(self, search=None, kind=None):

        if os.path.exists(self.db):
            self.logger.info('load from file')
            with open(self.db, 'r') as f:
                projects = json.load(f)
        else:
            self.logger.info('load from api')
            page = 1
            projects = []

            res = self.get('/projects?per_page=100&page=' + str(page)).json()

            while len(res) > 0:
                projects += res
                page += 1
                res = self.get('/projects?per_page=100&page=' + str(page)).json()

            projects = sorted(projects, key=lambda p: p['path_with_namespace'])

            with open(self.db, 'w') as f:
                json.dump(projects, f)

        if search:
            projects = [p for p in projects if re.search(search, p['path_with_namespace'], flags=re.IGNORECASE)]

        if kind:
            projects = [p for p in projects if p['namespace']['kind'] == kind]

        return projects

    def refresh_tags(self):
        projects = [self.get_latest_tag(p) for p in self.get_projects()]

        with open(self.db, 'w') as f:
            json.dump(projects, f)

    def reset(self):
        try:
            os.remove(self.db)
        except FileNotFoundError:
            self.logger.debug("nothing to reset")

    def get_latest_tag(self, p):
        res = self.get('/projects/' + str(p['id']) + '/repository/tags?order_by=name&search=^v').json()
        if len(res) == 0:
            res = self.get('/projects/' + str(p['id']) + '/repository/tags?order_by=name').json()
        if len(res) > 0:
            p['tag'] = res[0]['name']
            p['tag_created_at'] = res[0]['commit']['created_at'][0:10]
        return p
