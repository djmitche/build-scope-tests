"""
Common support code for scope tests
"""

import itertools
import gather
import difflib
import logging

log = logging.getLogger('common')

roles = gather.Roles()

# convert principals to "nice" names; TODO: all of these should be renamed
# upstream
_nice_names = {
    'client-id:QUUeaAazTAmU6F3Sc29zvQ': 'client-id-alias:permacred-armenzg-testing',
    'client-id:yHLBn3GaTY-SYhTnKw3X-Q': 'client-id-alias:temporary-credentials',
    'client-id:xMWxCdJpSriDz7zp7uFo8Q': 'client-id-alias:permacred-armenzg',
    'client-id:onvEnjW7Su6-53I7UhfCdg': 'client-id-alias:permacred-ted',
    'client-id:v9h-Fo_fQ3yq_-MeH6dP6w': 'client-id-alias:worker-ci-tests',
    'client-id:wQjAUsPgQ-OKuU8RWsz8tg': 'client-id-alias:permacred-nhirata',
    'client-id:XsQX5VRnSCi_gG1Fbby0AQ': 'client-id-alias:testdroid-worker',
    'client-id:eIy6aszeRQirIPOMwtOtqQ': 'client-id-alias:mozilla-taskcluster',
    'client-id:-69R5nFgQhmFalR2J3y9pA': 'client-id-alias:mozilla-taskcluster-ci',
    'client-id:HHb6HtDwQaS3dGdaa_j0ow': 'client-id-alias:funsize-scheduler',
    'client-id:MC7GCZfURkCGO8rS9KxgTg': 'client-id-alias:permacred-wcosta',
    'client-id:09tML-c8Tf6pYehxK8Rrpw': 'client-id-alias:permacred-bhearsum',
    'client-id:i8RcQ9nuRe-Q7mpVGnaHJg': 'client-id-alias:permacred-rail',
    'client-id:2YkrA35TSrCL9yOGDeW-Tg': 'client-id-alias:permacred-jhford',
    'client-id:2czfw97BQS6SvD-Q-F76Aw': 'client-id-alias:permacred-jonasfj',
    'client-id:7J6dLK6WS4WIUCUmsMssYw': 'client-id-alias:release-runner-dev',
    'client-id:DyUwCUOlRJWAOm7OJJWg1g': 'client-id-alias:permacred-garndt',
    'client-id:LY8eSq1WTb6qKMrWKGTvqw': 'client-id-alias:permacred-rthijssen',
    'client-id:LvL_9Z2FQLa2gO-3AgCQ_A': 'client-id-alias:permacred-selena',
    'client-id:N6l8rTzKRdCsLxXpboKNuw': 'client-id-alias:permacred-jlund',
    'client-id:XJhrEh8MSG-34W5qQjRadQ': 'client-id-alias:scheduler-taskcluster-net',
    'client-id:cVOkbX8TQu2UT7b-8VH0nA': 'client-id-alias:permacred-mrrrgn',
    'client-id:hkhwW8sQRFiau1ie1b29tQ': 'client-id-alias:permacred-pmoore',
    'client-id:iDpx218zTq6b8XoFMXssEw': 'client-id-alias:permacred-dustin',
    'client-id:sldk46fxR2CdSbiw2OR-4Q': 'client-id-alias:gaia-taskcluster-dev',
    'client-id:swn2Eg-pRu2h0ec3uNI9AQ': 'client-id-alias:queue-taskcluster-net',
    'client-id:u5Abj86VRsGmiagy6aO7Yw': 'client-id-alias:permacred-mshal',
    'client-id:xPK1XrauRn6v2QNMMIAOKg': 'client-id-alias:funsize-dev',
    'client-id:yMbwoZvhRout3T_Fr7h4Ng': 'client-id-alias:index-taskcluster-net',
    'client-id:kd-b_FdrSJ-4Gr3FF4IOpA': 'client-id-alias:gaia-taskcluster',
    'client-id:O6yB_zofTjCAjPSu4iYKoA': 'client-id-alias:taskcluster-github',
    'client-id:T9J-xA9JSUKQzfR99NRtMg': 'client-id-alias:mozilla-pulse-actions',
    'client-id:2NTE9AF4Qq2iNp_ZXan5DA': 'client-id-alias:npark',
    'client-id:Bx-Vfe_rSQ2HOtZQviwl_A': 'client-id-alias:sousmangoosta',
    'client-id:JmhqKvaWTHmnxmRqoORBaA': 'client-id-alias:brson',
    'client-id:LvhIONB6TAKCeZsbmrImrA': 'client-id-alias:gerard-majax',
    'client-id:_XwhECl7T_WBWcOdRQFVkA': 'client-id-alias:nullaus',
    'client-id:WX5WaEuzTwGh0Q-zpGSoWg': 'client-id-alias:rwood',
    'client-id:gEGWgxqgRZSikNXkDr6Tbw': 'client-id-alias:kgrandon',
    'client-id:kZ3PctbtSLml6PHw5YzTOw': 'client-id-alias:drs',
    'client-id:l-a4R0PXR4uHijZ4i7-kgw': 'client-id-alias:shako',
    'client-id:xu9LzAXBTRW8d3x_6Q-wCA': 'client-id-alias:mihneadb',
    'client-id:ycAM1VLgRA-677YJBT1K1w': 'client-id-alias:russn',
    'client-id:7biq0sFcRqGYGJ9juATLJA': 'client-id-alias:ffledgling',
}


def _nicer(principals):
    return set(_nice_names.get(p, p) for p in principals)

# trusted clients are relied on to perform actions on behalf of clients using
# temporary credentials or assumeScopes built from roles.  We treat the roles
# as principals and thus ignore the services implementing those roles.  Note
# that services which assign specific scopes, rather than roles, should NOT be
# listed here and must be handled directly in the tests.
_trusted_clients = set([
    # uses role `repo:hg.mozilla.org/$repo:*`
    'client-id-alias:mozilla-taskcluster',

    # uses roles `repo:github.com/$org/$repo:branch:$branch`
    # and `repo:github.com/$org/$repo:pull-request`
    'client-id-alias:gaia-taskcluster',
    'client-id-alias:gaia-taskcluster-dev',

    # uses role `repo:github.com/$org/$repo:pull-request`
    'client-id-alias:taskcluster-github',

    # uses role `hook-id:$hookId`
    'client-id:taskcluster-hooks',

    # issues temporary credentials to workers based on task.scopes, which
    # was validated when the task was defined, allowing no scope escalation
    # TODO: Bug 1228100
    'client-id:tc-queue',

    # issues temporary credentials to users based on their username and group
    # membership (`mozilla-user:*` and `mozilla-group:*`)
    'client-id:tc-login',

    # The aws-provisioner issues credentials to workers when it instantiates them
    'client-id:aws-provisioner',
])

# flatten down to a list of strings


def _flatten(l):
    def iter(l):
        if isinstance(l, basestring):
            return [l]
        else:
            return _flatten(l)
    return list(itertools.chain.from_iterable(iter(e) for e in l))


def _assertSetsMatch(got, exp, msg):
    if got != exp:
        diff = difflib.unified_diff(sorted(exp), sorted(got), lineterm="")
        raise AssertionError(msg + "\n" + "\n".join(diff))


def assertPrincipalsWithScope(scope, principals, omitTrusted=False):
    """Assert that the set of principals with the given scope is exactly as given; if
    omitTrusted is true, then the trusted clients listed in common.py are omitted; these
    clients are trusted pieces of TC infrastructure that carefully grant more restricted
    permissions using roles, as described in common.py"""
    got = _nicer(roles.principalsWithScope(scope))
    exp = _nicer(set(_flatten(principals)))
    if omitTrusted:
        got -= _trusted_clients
        exp -= _trusted_clients
    _assertSetsMatch(
        got, exp, "Got (+) a principal set different from expected (-):")


def assertPrincipalsWithRole(roleId, principals, exactMatch=True, omitTrusted=False):
    """Assert that the set of principals with the given role is exactly as
    given; if exactMatch is true, then the role is matched exactly, so
    principals with '*' or some prefix of the role will not be returned.  If
    exactMatch is false this is exactly like
    `assertPrincipalsWithScope('assume:' + roleId, principals)`."""
    if not exactMatch:
        return assertPrincipalsWithScope('assume:' + roleId, principals,
                                         omitTrusted=omitTrusted)
    got = _nicer(expandRole(roleId)) - set([roleId])
    exp = _nicer(set(_flatten(principals)))
    if omitTrusted:
        got -= _trusted_clients
        exp -= _trusted_clients
    _assertSetsMatch(
        got, exp, "Got (+) a principal set different from expected (-):")


def assertScopesWithPrefix(prefix, expectedScopes):
    """Assert that exactly the given scopes exist with the given prefix.  This
    is used to ensure that there are no scopes matching the pattern for which
    tests are not in place."""
    got = roles.scopesWithPrefix(prefix)
    for g in got:
        logging.debug('scope %s held by roles', g)
        for s in _nicer(roles.scopes[g]):
            logging.debug('  %s', s)
    exp = _nicer(set(expectedScopes))
    _assertSetsMatch(
        got, exp, "Got (+) a scope set different from expected (-):")


def expandRole(roleId):
    """Return the given role along with all roles that assume it"""
    return set([roleId] + [r.roleId for r in roles[roleId].assumedBy])
