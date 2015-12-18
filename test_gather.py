"""
Tests for the test hardness itself.  These tests do not depend on data in
TaskCluster, so if they fail, there is an issue with the test code.
"""

from nose.tools import eq_
import gather

old_listRoles = None
test_roles = {}

def setUpModule():
    global old_listRoles
    old_listRoles = gather.auth.listRoles
    def listRoles():
        global test_roles
        return [dict(roleId=r, expandedScopes=s) for r, s in test_roles.iteritems()]
    gather.auth.listRoles = listRoles

def tearDownModule():
    global old_listRoles
    gather.auth.listRoles = old_listRoles

def setTestRoles(roles):
    global test_roles
    test_roles = roles

def test_no_match():
    setTestRoles({'rr': ['bar']})
    eq_(gather.TaskCluster().principalsWithScope('foo'), set())

def test_straight_match():
    setTestRoles({'r1': ['foo', 'bar'], 'r2': ['foo', 'bing'], 'r3': ['baz']})
    eq_(gather.TaskCluster().principalsWithScope('foo'), set(['r1', 'r2']))

def test_star_in_role():
    setTestRoles({'r1': ['create:*'], 'r2': ['create:foo'], 'r3': ['create:bar']})
    eq_(gather.TaskCluster().principalsWithScope('create:bar'), set(['r1', 'r3']))

def test_star_in_scope():
    setTestRoles({'r1': ['create:*'], 'r2': ['create:foo'], 'r3': ['create:bar']})
    eq_(gather.TaskCluster().principalsWithScope('create:*'), set(['r1', 'r2', 'r3']))

def test_star_in_both():
    setTestRoles({'r1': ['cr*'], 'r2': ['create:*'], 'r3': ['create:foo']})
    eq_(gather.TaskCluster().principalsWithScope('create:*'), set(['r1', 'r2', 'r3']))

def test_scopesWithPrefix():
    setTestRoles({
        'r1': ['cr*'],
        'r2': ['create:*'],
        'r3': ['create:foo'],
        'r4': ['crea'],  # not a *-suffixed scope
        'r5': ['create:'],
    })
    eq_(gather.TaskCluster().scopesWithPrefix('create:'),
        set(['cr*', 'create:*', 'create:foo', 'create:']))

# TODO: inaccurate expandedScopes for star roles?
