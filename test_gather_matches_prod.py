"""
Tests checking that the expandedScopes calculation in gather.py matches that
used in production
"""

from nose.tools import assert_equal
from nose.plugins.skip import SkipTest
import gather

def test_matches():
    raise SkipTest("Bug 1220295")
    roles = gather.Roles()

    def _test(roleId):
        role = roles[roleId]
        assert_equal(sorted(role.expandedScopes), sorted(role.authExpandedScopes))

    for roleId in roles.roles:
        yield _test, roleId

assert_equal.__self__.maxDiff = None
