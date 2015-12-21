"""
Tests for scopes of interest to Release Engineering.

The idea is to know exactly who has which sorts of scopes, and detect any
changes in those lists.
"""

from common import assertPrincipalsWithScope
from common import principalsWith


def test_signing():
    assertPrincipalsWithScope("signing:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

        # user groups
        principalsWith('mozilla-group:releng'),
        principalsWith('mozilla-group:team_relops'),
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_bbb():
    assertPrincipalsWithScope("buildbot-bridge:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

        # user groups
        principalsWith('mozilla-group:releng'),
        principalsWith('mozilla-group:team_relops'),
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_bbb_tasks():
    """Buildbot Bridge (BBB) allows Buildbot jobs to be run via a TaskCluster
    task.  Most BBB tasks run without the need for additional scopes, but some
    more sensitive builders are restricted by `buildbot-bridge:..` scopes.  """
    assertPrincipalsWithScope("buildbot-bridge:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

        # user groups
        principalsWith('mozilla-group:releng'),
        principalsWith('mozilla-group:team_relops'),
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_bbb_worker():
    """Access to the Buildbot Bridge provisioner-id/worker-type allows
    scheduling of BBB jobs (but only on non-restricted builders unless there
    more scopes are also present)."""
    assertPrincipalsWithScope("queue:define-task:buildbot-bridge/*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

        'client-id-alias:mozilla-pulse-actions',  # armen's thing
        'client-id:bbb-scheduler',

        # people
        'client-id:adusca-development',

        # user groups
        principalsWith('mozilla-group:releng'),
        principalsWith('mozilla-group:team_relops'),
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_balrog_vpn():
    """Balrog is the administrative interface for Mozilla's update server, and
    automation uses it to publish information about new updates for download by
    end-users' updaters.  The BalrogVpnProxy docker-worker feature allows
    *network* access to Balrog.  It does not include any Balrog credentials.
    As such, it is but one layer of access control protecting Balrog, and is
    distributed a little more broadly than full access would be."""
    assertPrincipalsWithScope("docker-worker:feature:balrogVPNProxy", [
        # root
        'client-id:root',

        # CI testing
        'client-id-alias:worker-ci-tests',  # docker-worker integration tests

        # repos
        'moz-tree:level:3',
        'repo:hg.mozilla.org/integration/b2g-inbound:*',
        'repo:hg.mozilla.org/integration/fx-team:*',
        'repo:hg.mozilla.org/integration/mozilla-inbound:*',
        'repo:hg.mozilla.org/mozilla-central:*',
        'repo:hg.mozilla.org/releases/b2g-ota:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g34_v2_1s:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g44_v2_5:*',

        # AWS workers
        'worker-type:aws-provisioner-v1/*',  # Bug 1233555
        'client-id-alias:testdroid-worker',  # Bug 1218549

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net',  # Bug 1218541

        # people
        'client-id:dustin-docker-dev',

        # user groups
        principalsWith('mozilla-group:scm_level_3'),
        principalsWith('mozilla-group:releng'),
        principalsWith('mozilla-group:team_relops'),
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


# TODO: docker-worker caches
# TODO: queue:create-task:prov/wt
# TODO: queue:get-artifact:project/releng/*
# TODO: releng routes
# TODO: (new file?) auth stuff
# TODO: allowPtrace feature
