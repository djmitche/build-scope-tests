"""
Tests for scopes.
"""

from common import assertPrincipalsWithScope, permacreds

def test_signing():
    assertPrincipalsWithScope("signing:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',

        permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)

def test_bbb():
    assertPrincipalsWithScope("buildbot-bridge:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:release-runner-dev',
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',

        permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)
