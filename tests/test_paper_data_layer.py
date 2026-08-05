from __future__ import annotations

from closure.goel_operator import PolymeraseMode
from closure.paper_data_layer import (
    goel_mode_from_wuite_tension,
    load_catalog,
    paper_data_layer_digest,
    stack_declaration,
)


def test_catalog_is_not_rnd1_weights_only() -> None:
    stack = stack_declaration()
    assert stack["rnd1_weights_are_not_the_whole_external_stack"] is True
    assert stack["composition_rules"]["weights_optional"] is True
    assert "paper-derived architectures" in stack["stack"]["middle"]


def test_goel_and_open_datasets_are_catalogued() -> None:
    digest = paper_data_layer_digest()
    assert digest["goel_bound"]
    for required in (
        "opengenome2",
        "traitgym",
        "rnagym",
        "proteingym",
        "clinvar",
        "wuite-bustamante-tension-prior",
        "finite-goel-env-returns",
    ):
        assert required in digest["datasets"]
    assert "finite-goel-env-returns" in digest["local_ready_datasets"]
    assert "wuite-bustamante-tension-prior" in digest["local_ready_datasets"]


def test_wuite_tension_prior_drives_goel_modes() -> None:
    assert goel_mode_from_wuite_tension(6) is PolymeraseMode.POLYMERASE
    assert goel_mode_from_wuite_tension(34) is PolymeraseMode.STALLED
    assert goel_mode_from_wuite_tension(42) is PolymeraseMode.EXONUCLEASE


def test_catalog_papers_include_goel_and_evo2() -> None:
    catalog = load_catalog()
    ids = {row["id"] for row in catalog["paper_architectures"]}
    assert "goel-dna-environment-motor" in ids
    assert "evo2-opengenome2-runtime" in ids
    assert "rnd1-diffusion-language" in ids
    assert "omnii-reported-genome-lm" in ids
