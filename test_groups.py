"""
Tests for members of user groups.  With these tests in place, we can
safely use principalsWith(..) elsewhere.
"""

from common import assertPrincipalsWithRole
from common import principalsWith

taskcluster_permacreds = set([
    'client-id-alias:permacred-dustin',
    'client-id-alias:permacred-garndt',
    'client-id-alias:permacred-jhford',
    'client-id-alias:permacred-jonasfj',
    'client-id-alias:permacred-pmoore',
    'client-id-alias:permacred-selena',
    'client-id-alias:permacred-wcosta',
])

releng_permacreds = set([
    'client-id-alias:permacred-bhearsum',
    'client-id-alias:permacred-jlund',
    'client-id-alias:permacred-mrrrgn',
    'client-id-alias:permacred-mshal',
    'client-id-alias:permacred-rail',
])

relops_permacreds = set([
    'client-id-alias:permacred-dustin',
    'client-id-alias:permacred-rthijssen',
])


def test_releng():
    assertPrincipalsWithRole('mozilla-group:releng', [
        # all of the relengers
        releng_permacreds,

        # plus team_relops, because they're OK too
        principalsWith('mozilla-group:team_relops'),

        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_relops():
    assertPrincipalsWithRole('mozilla-group:team_relops', [
        relops_permacreds,

        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_taskcluster():
    assertPrincipalsWithRole('mozilla-group:team_taskcluster', [
        taskcluster_permacreds,
    ], omitTrusted=True)


def test_moco():
    assertPrincipalsWithRole('mozilla-group:team_moco', [
        'client-id-alias:temporary-credentials',  # Bug 1233553

        # everyone with a legacy permacred is considered an honorary moco
        # employee
        principalsWith('legacy-permacred'),

        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_scm_level_1():
    assertPrincipalsWithRole('mozilla-group:scm_level_1', [
        # a whole bunch of people "manually" granted this role
        'client-id-alias:brson',
        'client-id-alias:drs',
        'client-id-alias:gerard-majax',
        'client-id-alias:kgrandon',
        'client-id-alias:mihneadb',
        'client-id-alias:npark',
        'client-id-alias:nullaus',
        'client-id-alias:permacred-rthijssen',
        'client-id-alias:russn',
        'client-id-alias:rwood',
        'client-id-alias:shako',
        'client-id-alias:sousmangoosta',

        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_scm_level_2():
    assertPrincipalsWithRole('mozilla-group:scm_level_2', [
        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)


def test_scm_level_3():
    assertPrincipalsWithRole('mozilla-group:scm_level_3', [
        # a whole bunch of people "manually" granted this role
        'client-id-alias:permacred-armenzg',
        'client-id-alias:permacred-armenzg-testing',
        'client-id-alias:permacred-bhearsum',
        'client-id-alias:permacred-jlund',
        'client-id-alias:permacred-mrrrgn',
        'client-id-alias:permacred-mshal',
        'client-id-alias:permacred-nhirata',
        'client-id-alias:permacred-rail',
        'client-id-alias:permacred-ted',
        'client-id-alias:temporary-credentials',
        'client-id:gandalf',

        # taskcluster folks have *, hence matching this group
        principalsWith('mozilla-group:team_taskcluster'),
    ], omitTrusted=True)
