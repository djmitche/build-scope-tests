"""
Common support code for scope tests
"""

import gather
import difflib

roles = gather.TaskCluster()

# convert principals to "nice" names; TODO: all of these should be renamed
# upstream
_nice_names = {
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
}
def _nicer(principals):
    return set(_nice_names.get(p, p) for p in principals)

def assertPrincipalsWithScope(scope, principals):
    got = _nicer(roles.principalsWithScope(scope))
    exp = set(principals)
    if got != exp:
        diff = difflib.unified_diff(sorted(exp), sorted(got), lineterm="")
        raise AssertionError(
                "Got (+) a principal set different from expected (-):\n" +
                "\n".join(diff))

