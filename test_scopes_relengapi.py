"""
Tests for access to RelengAPI via docker-worker.

The docker-worker runs a proxy that grants access to RelengAPI based on scopes
(https://github.com/taskcluster/relengapi-proxy), so access to the relevant scopes
needs to be carefully controlled.

The permissions used by the proxy itself are also limited, but this is a
secondary layer of security.
"""

from common import assertPrincipalsWithScope
from common import assertScopesWithPrefix
from common import principalsWith


def test_relengapi_tooltool_download():
    """Docker-worker allows tooltool download permissions, for public or internal files, to repositories
    at all SCM levels including SCM level 1 (try).  This is necessary to build Firefox for Android, which
    requires non-public SDK and NDK bits."""
    print principalsWith('mozilla-group:scm_level_1'), 'moz-tree:level:1',
    for lvl in 'public', 'internal':
        assertPrincipalsWithScope("docker-worker:relengapi-proxy:tooltool.download." + lvl, [
            # trees
            principalsWith('moz-tree:level:1'),
            principalsWith('moz-tree:level:2'),
            principalsWith('moz-tree:level:3'),

            # permacreds used to download builds on bitbar
            'client-id-alias:testdroid-worker',

            # user groups that list the permission explicitly
            principalsWith('mozilla-group:releng'),

            # services
            'client-id-alias:funsize-dev',
            'client-id-alias:funsize-scheduler',
            'client-id-alias:release-runner-dev',
            'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

            # worker types
            'worker-type:aws-provisioner-v1/*',  # Bug 1233555

            # root
            'client-id:root',

            # CI testing
            'client-id:dustin-docker-dev',
            'client-id-alias:worker-ci-tests',  # docker-worker integration tests
        ], omitTrusted=True)


def test_relengapi_other_perms():
    """Only the relengapi permissions listed here appear anywhere in the roles"""
    assertScopesWithPrefix('docker-worker:relengapi-proxy:', [
        'docker-worker:relengapi-proxy:tooltool.download.internal',
        'docker-worker:relengapi-proxy:tooltool.download.public',
        'docker-worker:*',
        '*',  # trivial match
    ])
