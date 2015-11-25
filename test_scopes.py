"""
Tests for scopes of interest to Release Engineering.

The idea is to know exactly who has which sorts of scopes, and detect any
changes in those lists.
"""

from common import assertPrincipalsWithScope
from common import releng_permacreds
from common import taskcluster_permacreds

def test_signing():
    assertPrincipalsWithScope("signing:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net', # XXX Bug 1218541

        # people
        releng_permacreds,
        taskcluster_permacreds,

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
        'client-id-alias:scheduler-taskcluster-net', # XXX Bug 1218541

        # people
        releng_permacreds,
        taskcluster_permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
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
        'client-id-alias:scheduler-taskcluster-net', # XXX Bug 1218541

        # people
        releng_permacreds,
        taskcluster_permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
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
        'client-id-alias:scheduler-taskcluster-net', # XXX Bug 1218541

        'client-id-alias:mozilla-pulse-actions',  # armen's thing
        'client-id:bbb-scheduler',

        # people
        releng_permacreds,
        taskcluster_permacreds,
        'client-id:adusca-development',

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
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
        'client-id-alias:worker-ci-tests', # XXX ??

        # repos
        'mozilla-group:scm_level_3',
        'moz-tree:level:3',
        'repo:*',                           # TODO: don't list this, somehow
        'repo:hg.mozilla.org/integration/b2g-inbound:*',
        'repo:hg.mozilla.org/integration/fx-team:*',
        'repo:hg.mozilla.org/integration/mozilla-inbound:*',
        'repo:hg.mozilla.org/mozilla-central:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g34_v2_1s:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g44_v2_5:*',

        # all AWS workers
        'worker-type:aws-provisioner-v1/*', # XXX ??
        'client-id-alias:testdroid-worker', # XXX ??

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net', # XXX Bug 1218541
        'client-id:aws-provisioner',  # XXX ??

        # people
        releng_permacreds,
        taskcluster_permacreds,
        'client-id-alias:permacred-armenzg',
        'client-id-alias:permacred-armenzg-testing',
        'client-id-alias:permacred-nhirata',
        'client-id-alias:permacred-ted',
        'client-id-alias:temporary-credentials',  # XXX will go away
        'client-id:gandalf',

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)

# TODO: relengapi-proxy
# TODO: docker-worker caches
# TODO: queue:create-task:prov/wt
# TODO: queue:get-artifact:project/releng/*
# TODO: releng routes
# TODO: (new file?) auth stuff
