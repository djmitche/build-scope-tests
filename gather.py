import taskcluster

auth = taskcluster.Auth()

class TaskCluster(object):

    def __init__(self):
        self.load()

    def load(self):
        roles = auth.listRoles()
        self.roles = {r['roleId']: r['expandedScopes'] for r in roles}
        self.scopes = scopes = {}
        for r in roles:
            for s in r['expandedScopes']:
                scopes.setdefault(s, set()).add(r['roleId'])

    def principalsWithScope(self, scope):
        if scope.endswith('*'):
            scope = scope[:-1]
            def check(s):
                return s.startswith(scope) or (s.endswith('*') and scope.startswith(s[:-1]))
        else:
            def check(s):
                return s == scope or (s.endswith('*') and scope.startswith(s[:-1]))

        return set(role for role, scopes in self.roles.iteritems() if any(check(s) for s in scopes))
