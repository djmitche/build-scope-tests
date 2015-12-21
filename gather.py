import taskcluster
from memoized_property import memoized_property

auth = taskcluster.Auth()

# NOTE: the algorithms in this file are godawful slow.  That's OK!  They're
# also very simple, and if they agree with the more complex implementation
# in the auth service, then we can be confident that it is correct, too.
# Unless tests are taking hours to run, do not replace these algorithms with
# more complex versions.

def _starmatch(x, y):
    """Return true if x == y or x is a star-suffixed prefix of y"""
    if x == y:
        return True
    else:
        return x[-1] == '*' and y.startswith(x[:-1])

class Role(object):

    def __init__(self, r):
        self.roleId = r['roleId']
        self.scopes = r['scopes']
        self.authExpandedScopes = r['expandedScopes']

        self.children = []
        self.parents = []

    @memoized_property
    def assumedBy(self):
        rv = set()
        self._assumedByIterator(rv)
        return rv

    def _assumedByIterator(self, accumulator):
        for p in self.parents:
            if p not in accumulator:
                accumulator.add(p)
                p._assumedByIterator(accumulator)

    @memoized_property
    def assumes(self):
        rv = set()
        self._assumesIterator(rv)
        return rv

    def _assumesIterator(self, accumulator):
        for p in self.children:
            if p not in accumulator:
                accumulator.add(p)
                p._assumesIterator(accumulator)

    @memoized_property
    def expandedScopes(self):
        scopes = set(self.scopes)
        scopes.add('assume:' + self.roleId)
        for r in self.assumes:
            scopes |= set(r.scopes)
        # normalize (slowly)
        rv = set()
        for scope in scopes:
            for otherscope in scopes:
                if scope != otherscope and _starmatch(otherscope, scope):
                    break
            else:
                rv.add(scope)
        return rv

class Roles(object):

    def __init__(self):
        self.load()

    def load(self):
        roles = auth.listRoles()
        self.roles = {r['roleId']: Role(r) for r in roles}

        # connect all of the parent and child relationships between roles, including
        # star expansion of roles
        for r in self.roles.itervalues():
            for s in r.scopes:
                if s.startswith('assume:'):
                    ref = s[7:]
                    for cr in self.roles.itervalues():
                        if _starmatch(ref, cr.roleId) or _starmatch(cr.roleId, ref):
                            r.children.append(cr)
                            cr.parents.append(r)

        # Map scopes to the roles that contain them (with star expansion and
        # normalization)
        # scopepattern -> [roleId, ..]
        self.scopes = scopes = {}
        for r in self.roles.itervalues():
            for s in r.expandedScopes:
                scopes.setdefault(s, set()).add(r.roleId)

    def __getitem__(self, k):
        return self.roles[k]

    def expandAssumptions(self, scopes):
        """Expand the list of scopes to include the roles that it assumes (but
        not the scopes, or any other roles, implied by those roles)."""
        res = set(scopes)
        for s in scopes:
            if s.startswith('assume:'):
                res.extend(self.assumes.get(s[7:], []))
        return res

    def expandAssumers(self, scopes):
        """Expand the list of scopes to include the roles assuming any roles in the list."""
        res = set(scopes)
        for s in scopes:
            if s.startswith('assume:'):
                res.extend(self.assumedBy.get(s[7:], []))
        return res

    def scopesWithPrefix(self, prefix):
        """Return all scopes with the given prefix, or which prefix satisfies"""
        return set(s for s in self.scopes if s.startswith(prefix) or (s.endswith('*') and prefix.startswith(s[:-1])))


    def principalsWithScope(self, scope):
        """Return the list of principals which satisfy the given scope"""
        if scope.endswith('*'):
            scope = scope[:-1]
            def check(s):
                return s.startswith(scope) or (s.endswith('*') and scope.startswith(s[:-1]))
        else:
            def check(s):
                return s == scope or (s.endswith('*') and scope.startswith(s[:-1]))

        return set(role.roleId for role in self.roles.itervalues()
                   if any(check(s) for s in role.expandedScopes))
