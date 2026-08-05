from __future__ import annotations

import json
from pathlib import Path

from closure.dataset_adapters import (
    CACHE_ROOT,
    episodes_from_clinvar,
    episodes_from_opengenome2_style,
    episodes_from_proteingym,
    episodes_from_rnagym,
    episodes_from_traitgym,
    load_all_open_episodes,
)
from closure.paper_data_layer import paper_data_layer_digest
from closure.return_unified_runtime import architecture_from_system, reunify_episode


def _write_minimal_caches(tmp_path: Path) -> None:
    (tmp_path / "traitgym").mkdir(parents=True)
    (tmp_path / "traitgym" / "mendelian_traits_test_sample.json").write_text(
        json.dumps(
            {
                "fetched_at": "test",
                "rows": [
                    {
                        "chrom": "1",
                        "pos": 100,
                        "ref": "A",
                        "alt": "G",
                        "label": True,
                        "consequence": "PLS",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "rnagym").mkdir()
    (tmp_path / "rnagym" / "fitness_sample.json").write_text(
        json.dumps(
            {
                "rows": [
                    {"mutant": "A1G", "dms_score": "0.5", "sequence": "AUCG" * 20}
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "clinvar").mkdir()
    (tmp_path / "clinvar" / "brca1_pathogenic_sample.json").write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "uid": "1",
                        "accession": "VCV1",
                        "title": "BRCA1 test",
                        "obj_type": "Variant",
                        "variation_set": [],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "proteingym").mkdir()
    (tmp_path / "proteingym" / "reference_substitutions_sample.json").write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "DMS_id": "TEST_DMS",
                        "UniProt_ID": "P12345",
                        "taxon": "Virus",
                        "seq_len": "40",
                        "molecule_name": "test",
                        "source_organism": "test",
                        "selection_assay": "growth",
                        "target_seq_prefix": "M" * 40,
                        "target_seq_len": 40,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "opengenome2").mkdir()
    seq = "ATGCGTACGT" * 20
    (tmp_path / "opengenome2" / "ncbi_genomic_context_sample.json").write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "label": "test",
                        "accession": "NC_TEST",
                        "start": 1,
                        "stop": len(seq),
                        "header": ">test",
                        "sequence": seq,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_episode_builders_from_cached_samples(tmp_path: Path, monkeypatch) -> None:
    _write_minimal_caches(tmp_path)
    monkeypatch.setattr("closure.dataset_adapters.CACHE_ROOT", tmp_path)

    assert len(episodes_from_traitgym()) == 1
    assert len(episodes_from_rnagym()) == 1
    assert len(episodes_from_clinvar()) == 1
    assert len(episodes_from_proteingym()) == 1
    assert len(episodes_from_opengenome2_style()) == 2  # seq + gene

    episodes = load_all_open_episodes()
    assert len(episodes) == 6
    architecture = architecture_from_system(
        {
            "id": "bio-closure-independent",
            "family": "black-mirror-closure",
            "biological_native": True,
            "open_weights": False,
            "adapter": "closure.independent_model:UnifiedClosureArchitecturalLoop",
        },
        weights_available=True,
    )
    for episode in episodes:
        receipt = reunify_episode(architecture, episode)
        assert receipt.joint_arm_status == "VERIFIED"
        assert receipt.write_back_allowed


def test_paper_digest_sees_cache_when_present(tmp_path: Path, monkeypatch) -> None:
    _write_minimal_caches(tmp_path)
    monkeypatch.setattr("closure.dataset_adapters.CACHE_ROOT", tmp_path)
    digest = paper_data_layer_digest()
    for ds in ("traitgym", "rnagym", "clinvar", "proteingym", "opengenome2"):
        assert ds in digest["local_ready_datasets"]
        assert ds in digest["cached_online_samples"]
