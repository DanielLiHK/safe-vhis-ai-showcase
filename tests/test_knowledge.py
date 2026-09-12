from safe_vhis.knowledge import load_cases, load_sources, retrieve


def test_dataset_is_small_and_fixed() -> None:
    cases = load_cases()
    assert len(cases) == 12
    assert len({case.id for case in cases}) == 12


def test_retrieval_finds_renewal_source() -> None:
    result = retrieve("保證續保到100歲？", load_sources())
    assert result
    assert result[0].id == "VHIS-P01-RENEWAL"


def test_all_gold_source_ids_exist() -> None:
    source_ids = {source.id for source in load_sources()}
    for case in load_cases():
        assert set(case.gold_source_ids).issubset(source_ids)

