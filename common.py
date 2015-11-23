"""
Common support code for scope tests
"""

import itertools
import gather
import difflib

roles = gather.TaskCluster()

# convert principals to "nice" names; TODO: all of these should be renamed
# upstream
_nice_names = {
    'client-id:-69R5nFgQhmFalR2J3y9pA': 'client-id-alias:mozilla-taskcluster',
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
    'clietn-id:O6yB_zofTjCAjPSu4iYKoA': 'client-id-alias:taskcluster-github',
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
])

# flatten down to a list of strings
def _flatten(l):
    def iter(l):
        if isinstance(l, basestring):
            return [l]
        else:
            return _flatten(l)
    return list(itertools.chain.from_iterable(iter(e) for e in l))

def assertPrincipalsWithScope(scope, principals, omitTrusted=False):
    got = _nicer(roles.principalsWithScope(scope))
    if omitTrusted:
        got -= _trusted_clients
    exp = set(_flatten(principals))
    if got != exp:
        diff = difflib.unified_diff(sorted(exp), sorted(got), lineterm="")
        raise AssertionError(
                "Got (+) a principal set different from expected (-):\n" +
                "\n".join(diff))


permacreds = set([
    'client-id-alias:permacred-bhearsum',
    'client-id-alias:permacred-dustin',
    'client-id-alias:permacred-garndt',
    'client-id-alias:permacred-jhford',
    'client-id-alias:permacred-jlund',
    'client-id-alias:permacred-jonasfj',
    'client-id-alias:permacred-mrrrgn',
    'client-id-alias:permacred-mshal',
    'client-id-alias:permacred-pmoore',
    'client-id-alias:permacred-rail',
    'client-id-alias:permacred-rthijssen',
    'client-id-alias:permacred-selena',
    'client-id-alias:permacred-wcosta',
])
