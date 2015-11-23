"""
Tests for scopes.
"""

from common import assertPrincipalsWithScope

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

        # perma-creds
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

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)
