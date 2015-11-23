"""
Tests for scopes.
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
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',

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
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',

        # people
        releng_permacreds,
        taskcluster_permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)


def test_bbb_tasks():
    # TODO: worker-type for bbb
    assertPrincipalsWithScope("buildbot-bridge:*", [
        # root
        'client-id:root',

        # services
        'client-id-alias:release-runner-dev',
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',

        # people
        releng_permacreds,
        taskcluster_permacreds,

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',
    ], omitTrusted=True)


def test_balrog():
    # TODO: https://bugzilla.mozilla.org/show_bug.cgi?id=1220692
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
        'client-id-alias:release-runner-dev',
        'client-id:tc-login',
        'client-id:tc-queue',
        'client-id-alias:scheduler-taskcluster-net',
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id:aws-provisioner',

        # people
        releng_permacreds,
        taskcluster_permacreds,
        'client-id-alias:permacred-armenzg',
        'client-id-alias:permacred-armenzg-testing',
        'client-id-alias:permacred-nhirata',
        'client-id-alias:permacred-ted',
        'client-id-alias:temporary-credentials',
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
