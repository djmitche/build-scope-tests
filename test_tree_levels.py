"""
Tests for access to the moz-tree:level:* roles
"""

from common import assertPrincipalsWithRole
from common import principalsWith

l1_repos = [
    'repo:hg.mozilla.org/try:*',
]

l2_repos = [
    'repo:hg.mozilla.org/projects/alder:*',
    'repo:hg.mozilla.org/projects/cedar:*',
    'repo:hg.mozilla.org/projects/cypress:*',
    'repo:hg.mozilla.org/projects/pine:*',
]

l3_repos = [
    'repo:hg.mozilla.org/integration/b2g-inbound:*',
    'repo:hg.mozilla.org/integration/fx-team:*',
    'repo:hg.mozilla.org/integration/mozilla-inbound:*',
    'repo:hg.mozilla.org/mozilla-central:*',
    'repo:hg.mozilla.org/releases/b2g-ota:*',
    'repo:hg.mozilla.org/releases/mozilla-b2g34_v2_1s:*',
    'repo:hg.mozilla.org/releases/mozilla-b2g44_v2_5:*',
]

def test_tree_level_3():
    assertPrincipalsWithRole('moz-tree:level:3', [
        # level-3 people and repos
        principalsWith('mozilla-group:scm_level_3'), l3_repos,

        # CI testing
        'client-id:dustin-docker-dev',
        'client-id-alias:worker-ci-tests',  # docker-worker integration tests

        # permacreds used to download builds on bitbar
        'client-id-alias:testdroid-worker',  # Bug 1218549

        # services
        'client-id:aws-provisioner',

        # worker types
        'worker-type:aws-provisioner-v1/*',  # Bug 1233555
    ], omitTrusted=True)

def test_tree_level_2():
    assertPrincipalsWithRole('moz-tree:level:2', [
        # level 3, plus level-2 people and repos
        principalsWith('mozilla-group:scm_level_2'), l2_repos,
        principalsWith('moz-tree:level:3'),
    ], omitTrusted=True)

def test_tree_level_1():
    assertPrincipalsWithRole('moz-tree:level:1', [
        # level 2, plus level-2 people and repos
        principalsWith('mozilla-group:scm_level_1'), l1_repos,
        principalsWith('moz-tree:level:2'),
    ], omitTrusted=True)
