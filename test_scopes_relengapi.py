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
from common import releng_permacreds
from common import taskcluster_permacreds

def test_relengapi_tooltool_download_public():
    """Some repos have download the ability to download public artifacts from
    tooltool.  Since this operation can occur without credntials, too, it need
    not be highly restricted."""
    assertPrincipalsWithScope("docker-worker:relengapi-proxy:tooltool.download.public", [
        # root
        'client-id:root',

        # CI testing
        'client-id-alias:worker-ci-tests', # docker-worker integration tests

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net', # Bug 1218541

        # trees
        'moz-tree:level:1',
        'moz-tree:level:2',
        'moz-tree:level:3',
        'mozilla-group:scm_level_1',
        'mozilla-group:scm_level_2',
        'mozilla-group:scm_level_3',

        # repos
        'repo:*',
        'repo:hg.mozilla.org/integration/b2g-inbound:*',
        'repo:hg.mozilla.org/integration/fx-team:*',
        'repo:hg.mozilla.org/integration/mozilla-inbound:*',
        'repo:hg.mozilla.org/mozilla-central:*',
        'repo:hg.mozilla.org/projects/alder:*',
        'repo:hg.mozilla.org/projects/cedar:*',
        'repo:hg.mozilla.org/projects/cypress:*',
        'repo:hg.mozilla.org/projects/pine:*',
        'repo:hg.mozilla.org/releases/b2g-ota:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g34_v2_1s:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g44_v2_5:*',
        'repo:hg.mozilla.org/try:*',

        # people
        releng_permacreds,
        taskcluster_permacreds,
        'client-id:dustin-docker-dev',
        'client-id-alias:permacred-armenzg',
        'client-id-alias:permacred-armenzg-testing',
        'client-id-alias:permacred-nhirata',
        'client-id-alias:permacred-ted',
        'client-id-alias:temporary-credentials',
        'client-id-alias:testdroid-worker',
        'client-id-alias:npark',
        'client-id-alias:sousmangoosta',
        'client-id-alias:brson',
        'client-id-alias:gerard-majax',
        'client-id-alias:rwood',
        'client-id-alias:nullaus',
        'client-id-alias:kgrandon',
        'client-id-alias:drs',
        'client-id-alias:shako',
        'client-id-alias:mihneadb',
        'client-id-alias:russn',
        'client-id:gandalf',

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',

        # services
        'client-id:aws-provisioner',

        # worker types
        'worker-type:aws-provisioner-v1/*', # Bug 1233555
        'worker-type:aws-provisioner-v1/gaia-decision', # Bug 1233555
        'worker-type:aws-provisioner-v1/gecko-decision', # Bug 1233555

        # Bug 1220295
        'repo:*',
    ], omitTrusted=True)

def test_relengapi_tooltool_download_internal():
    """Some repos have download the ability to download internal artifacts
    from tooltool.  This extends to try-level repositories."""
    assertPrincipalsWithScope("docker-worker:relengapi-proxy:tooltool.download.internal", [
        # root
        'client-id:root',

        # CI testing
        'client-id-alias:worker-ci-tests', # docker-worker integration tests

        # services
        'client-id-alias:funsize-dev',
        'client-id-alias:funsize-scheduler',
        'client-id-alias:release-runner-dev',
        'client-id-alias:scheduler-taskcluster-net', # Bug 1218541

        # trees
        'moz-tree:level:1',
        'moz-tree:level:2',
        'moz-tree:level:3',
        'mozilla-group:scm_level_1',
        'mozilla-group:scm_level_2',
        'mozilla-group:scm_level_3',

        # repos
        'repo:*',
        'repo:hg.mozilla.org/integration/b2g-inbound:*',
        'repo:hg.mozilla.org/integration/fx-team:*',
        'repo:hg.mozilla.org/integration/mozilla-inbound:*',
        'repo:hg.mozilla.org/mozilla-central:*',
        'repo:hg.mozilla.org/projects/alder:*',
        'repo:hg.mozilla.org/projects/cedar:*',
        'repo:hg.mozilla.org/projects/cypress:*',
        'repo:hg.mozilla.org/projects/pine:*',
        'repo:hg.mozilla.org/releases/b2g-ota:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g34_v2_1s:*',
        'repo:hg.mozilla.org/releases/mozilla-b2g44_v2_5:*',
        'repo:hg.mozilla.org/try:*',

        # people
        releng_permacreds,
        taskcluster_permacreds,
        'client-id:dustin-docker-dev',
        'client-id-alias:permacred-armenzg',
        'client-id-alias:permacred-armenzg-testing',
        'client-id-alias:permacred-nhirata',
        'client-id-alias:permacred-ted',
        'client-id-alias:temporary-credentials',
        'client-id-alias:testdroid-worker',
        'client-id-alias:npark',
        'client-id-alias:sousmangoosta',
        'client-id-alias:brson',
        'client-id-alias:gerard-majax',
        'client-id-alias:rwood',
        'client-id-alias:nullaus',
        'client-id-alias:kgrandon',
        'client-id-alias:drs',
        'client-id-alias:shako',
        'client-id-alias:mihneadb',
        'client-id-alias:russn',
        'client-id:gandalf',

        # user groups
        'mozilla-group:releng',
        'mozilla-group:team_relops',
        'mozilla-group:team_taskcluster',

        # services
        'client-id:aws-provisioner',

        # worker types
        'worker-type:aws-provisioner-v1/*', # Bug 1233555
        'worker-type:aws-provisioner-v1/gaia-decision', # Bug 1233555
        'worker-type:aws-provisioner-v1/gecko-decision', # Bug 1233555

        # Bug 1220295
        'repo:*',
    ], omitTrusted=True)

def test_relengapi_other_perms():
    """Only the relengapi permissions listed here appear anywhere in the roles"""
    assertScopesWithPrefix('docker-worker:relengapi-proxy:', [
        'docker-worker:relengapi-proxy:tooltool.download.internal',
        'docker-worker:relengapi-proxy:tooltool.download.public',
        'docker-worker:*',
        '*',  # trivial match
    ]);
