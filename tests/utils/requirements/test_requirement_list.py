from macta_tools.utils.requirements import EqualityRequirement, RequirementList


def test_basic_rqlist() -> None:
    """Tests that a basic valid `RequirementList` works"""

    rqlist = RequirementList({
        'annot_type': EqualityRequirement('marker'),
    })

    assert rqlist.check(annot_type='marker')
    assert not rqlist.check(annot_type='ref')
    assert rqlist.check(**{'annot_type': 'marker'})
    assert not rqlist.check(**{'annot_type': 'ref'})
