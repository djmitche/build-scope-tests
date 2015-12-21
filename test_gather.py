"""
Tests for the test hardness itself.  These tests do not depend on data in
TaskCluster, so if they fail, there is an issue with the test code.
"""

from nose.tools import eq_
import gather

old_listRoles = None
testRoles = {}

commonTestRoles = {
    # role graph with no stars
    'r1a': ['assume:r2a'],
    'r1b': ['assume:r2a'],
    'r1c': ['assume:r2b'],
    'r2a': ['assume:r3a'],
    'r2b': ['assume:r3a'],
    'r3a': ['assume:r4a', 'assume:r4b'],
    'r4a': [],
    'r4b': ['assume:r5a', 'assume:r5b'],  # NOTE: there is no r5b
    'r5a': [],

    # role graph with stars
    'client:foo': ['assume:repo:github.com/foo/*', 'assume:group:coolpeople'],
    'client:bar': ['assume:repo:github.com/bar/*', 'assume:hook:abc/def'],
    'repo:github.com/*': [],
    'repo:github.com/foo/somerepo': [],
    'group:coolpeople': ['assume:hook:abc/*'],
    'hook:*': [],
    'hook:abc/*': [],
    'hook:abc/def': [],
    'hook:abc/efg': [],
}

def setUpModule():
    global old_listRoles
    old_listRoles = gather.auth.listRoles
    def listRoles():
        global testRoles
        return testRoles
    gather.auth.listRoles = listRoles

def tearDownModule():
    global old_listRoles
    gather.auth.listRoles = old_listRoles

def setTestRoles(roles):
    global testRoles
    # expand the roles out into the return value of listRoles
    testRoles = []
    for roleId, scopes in roles.iteritems():
        testRoles.append({
            'roleId': roleId,
            'scopes': scopes,
            'expandedScopes': [],  # not used here
        })
    return gather.Roles()

def test_no_match():
    roles = setTestRoles({'rr': ['bar']})
    eq_(roles.principalsWithScope('foo'), set())

def test_straight_match():
    roles = setTestRoles({'r1': ['foo', 'bar'], 'r2': ['foo', 'bing'], 'r3': ['baz']})
    eq_(roles.principalsWithScope('foo'), set(['r1', 'r2']))

def test_star_in_role():
    roles = setTestRoles({'r1': ['create:*'], 'r2': ['create:foo'], 'r3': ['create:bar']})
    eq_(roles.principalsWithScope('create:bar'), set(['r1', 'r3']))

def test_star_in_scope():
    roles = setTestRoles({'r1': ['create:*'], 'r2': ['create:foo'], 'r3': ['create:bar']})
    eq_(roles.principalsWithScope('create:*'), set(['r1', 'r2', 'r3']))

def test_star_in_both():
    roles = setTestRoles({'r1': ['cr*'], 'r2': ['create:*'], 'r3': ['create:foo']})
    eq_(roles.principalsWithScope('create:*'), set(['r1', 'r2', 'r3']))

def test_scopesWithPrefix():
    roles = setTestRoles({
        'r1': ['cr*'],
        'r2': ['create:*'],
        'r3': ['create:foo'],
        'r4': ['crea'],  # not a *-suffixed scope
        'r5': ['create:'],
    })
    print roles['r5'].expandedScopes
    eq_(roles.scopesWithPrefix('create:'),
        set(['cr*', 'create:*', 'create:foo', 'create:']))

def test_role_dag():
    roles = setTestRoles(commonTestRoles)

    def pc(role, parents, children):
        print("%s parents %s children %s" % (role, parents, children))
        eq_(sorted(r.roleId for r in roles[role].parents), sorted(parents))
        eq_(sorted(r.roleId for r in roles[role].children), sorted(children))

    pc('r1a', [], ['r2a'])
    pc('r1b', [], ['r2a'])
    pc('r1c', [], ['r2b'])
    pc('r2a', ['r1a', 'r1b'], ['r3a'])
    pc('r2b', ['r1c'], ['r3a'])
    pc('r3a', ['r2a', 'r2b'], ['r4a', 'r4b'])
    pc('r4a', ['r3a'], [])
    pc('r4b', ['r3a'], ['r5a'])
    pc('r5a', ['r4b'], [])

    pc('client:foo', [], [
        'repo:github.com/*',
        'repo:github.com/foo/somerepo',
        'group:coolpeople',
    ])
    pc('client:bar', [], [
        'repo:github.com/*',
        'hook:*',
        'hook:abc/*',
        'hook:abc/def',
    ])
    pc('repo:github.com/*', ['client:foo', 'client:bar'], [])
    pc('repo:github.com/foo/somerepo', ['client:foo'], [])
    pc('group:coolpeople', ['client:foo'], [
        'hook:*',
        'hook:abc/*',
        'hook:abc/def',
        'hook:abc/efg',
    ])
    pc('hook:*', ['group:coolpeople', 'client:bar'], [])
    pc('hook:abc/*', ['group:coolpeople', 'client:bar'], [])
    pc('hook:abc/def', ['group:coolpeople', 'client:bar'], [])
    pc('hook:abc/efg', ['group:coolpeople'], [])

def test_role_assumedBy():
    roles = setTestRoles(commonTestRoles)
    def check(roleId, assumedBy):
        print("roleId %s assumedBy %s" % (roleId, assumedBy))
        eq_(sorted([r.roleId for r in roles[roleId].assumedBy]),
            sorted(assumedBy))
    check('group:coolpeople', ['client:foo'])
    check('hook:*', ['client:foo', 'client:bar', 'group:coolpeople'])
    check('hook:abc/efg', ['client:foo', 'group:coolpeople'])

def test_role_assumptioni_recursive():
    roles = setTestRoles({
        'r1': ['assume:r2'],
        'r2': ['assume:r1'],
    })
    eq_(sorted([r.roleId for r in roles['r1'].assumedBy]),
        sorted(['r1', 'r2']))
    eq_(sorted([r.roleId for r in roles['r1'].assumes]),
        sorted(['r1', 'r2']))

def test_role_assumes():
    roles = setTestRoles(commonTestRoles)
    def check(roleId, assumes):
        print("roleId %s assumes %s" % (roleId, assumes))
        eq_(sorted([r.roleId for r in roles[roleId].assumes]),
            sorted(assumes))
    check('group:coolpeople', [
        'hook:abc/*',
        'hook:*',
        'hook:abc/def',
        'hook:abc/efg',
    ])
    check('client:foo', [
        'hook:*',
        'hook:abc/*',
        'hook:abc/def',
        'hook:abc/efg',
        'repo:github.com/*',
        'repo:github.com/foo/somerepo',
        'group:coolpeople',
    ])

def test_role_expandedScopes():
    roles = setTestRoles({
        'r1': ['some:scope', 'assume:r2'],
        'r2': ['another:scope', 'assume:r3'],
    })
    eq_(sorted(roles['r1'].expandedScopes), sorted([
        'assume:r1',
        'assume:r2',
        'assume:r3',
        'some:scope',
        'another:scope',
    ]))

def test_role_expandedScopes_normalized():
    roles = setTestRoles({
        'r1': ['some:scope', 'assume:r2'],
        'r2': ['another:scope', 'some:other:scope', 'assume:r3'],
        'r3': ['some:*'],
    })
    eq_(sorted(roles['r1'].expandedScopes), sorted([
        'assume:r1',
        'assume:r2',
        'assume:r3',
        'some:*',
        'another:scope',
    ]))
