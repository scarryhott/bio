# Copyright 2026 scarryhott/bio contributors.
"""Download / online-service adapters for catalogued open biological datasets.

Fetches small held-out return samples via Hugging Face datasets-server and NCBI
E-utilities, caches them locally, and lifts rows into return-unified episodes
for our Closure AGI. Full OpenGenome2 corpus is not mirrored (multi-GB shards);
sequence-likelihood / gene-completion use NCBI nucleotide online under the
OpenGenome2 benchmark family with explicit provenance.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .biology import BiologicalEpisode
from .digest import digest
from .return_unified_runtime import ReturnUnifiedEpisodeSpec

ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = ROOT / "benchmarks" / "data_cache"
DEFAULT_USER_AGENT = "bio-closure-agi/0.1 (dataset-adapter; research; local-cache)"


@dataclass(frozen=True)
class DatasetFetchReceipt:
    dataset_id: str
    source: str
    transport: str
    local_path: str
    n_rows: int
    fetched_at: str
    epistemic_status: str
    license_note: str
    provenance: dict[str, Any] = field(default_factory=dict)
    ok: bool = True
    detail: str = ""


def _http_get_json(url: str, *, timeout: float = 60.0) -> Any:
    req = Request(url, headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _http_get_text(url: str, *, timeout: float = 60.0) -> str:
    req = Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def cache_manifest_path() -> Path:
    return CACHE_ROOT / "manifest.json"


def load_cache_manifest() -> dict[str, Any]:
    path = cache_manifest_path()
    if not path.exists():
        return {"schema_version": "1.0", "datasets": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def _update_manifest(receipt: DatasetFetchReceipt) -> None:
    manifest = load_cache_manifest()
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest.setdefault("datasets", {})[receipt.dataset_id] = {
        "source": receipt.source,
        "transport": receipt.transport,
        "local_path": receipt.local_path,
        "n_rows": receipt.n_rows,
        "fetched_at": receipt.fetched_at,
        "epistemic_status": receipt.epistemic_status,
        "license_note": receipt.license_note,
        "provenance": receipt.provenance,
        "ok": receipt.ok,
        "detail": receipt.detail,
    }
    _write_json(cache_manifest_path(), manifest)


def fetch_traitgym_sample(*, n: int = 3, force: bool = False) -> DatasetFetchReceipt:
    """Fetch TraitGym mendelian_traits test rows via HF datasets-server."""

    out = CACHE_ROOT / "traitgym" / "mendelian_traits_test_sample.json"
    source = (
        "https://datasets-server.huggingface.co/rows?"
        + urlencode(
            {
                "dataset": "songlab/TraitGym",
                "config": "mendelian_traits",
                "split": "test",
                "offset": "0",
                "length": str(n),
            }
        )
    )
    if out.exists() and not force:
        data = json.loads(out.read_text(encoding="utf-8"))
        receipt = DatasetFetchReceipt(
            dataset_id="traitgym",
            source=source,
            transport="huggingface-datasets-server",
            local_path=str(out.relative_to(ROOT)),
            n_rows=len(data.get("rows", [])),
            fetched_at=str(data.get("fetched_at", "")),
            epistemic_status="CACHED_ONLINE_SAMPLE",
            license_note="TraitGym MIT (songlab/TraitGym); sample only",
            provenance=dict(data.get("provenance") or {}),
            detail="cache hit",
        )
        _update_manifest(receipt)
        return receipt

    payload = _http_get_json(source)
    rows = [item["row"] for item in payload.get("rows", [])]
    fetched_at = datetime.now(timezone.utc).isoformat()
    envelope = {
        "dataset_id": "traitgym",
        "hf_dataset": "songlab/TraitGym",
        "config": "mendelian_traits",
        "split": "test",
        "fetched_at": fetched_at,
        "source": source,
        "provenance": {
            "api": "huggingface datasets-server",
            "revision_note": "live server rows; not a pinned git SHA of the parquet",
        },
        "rows": rows,
    }
    _write_json(out, envelope)
    receipt = DatasetFetchReceipt(
        dataset_id="traitgym",
        source=source,
        transport="huggingface-datasets-server",
        local_path=str(out.relative_to(ROOT)),
        n_rows=len(rows),
        fetched_at=fetched_at,
        epistemic_status="DOWNLOADED_ONLINE_SAMPLE",
        license_note="TraitGym MIT (songlab/TraitGym); sample only",
        provenance=envelope["provenance"],
    )
    _update_manifest(receipt)
    return receipt


def fetch_rnagym_sample(*, n: int = 3, force: bool = False) -> DatasetFetchReceipt:
    """Fetch RNAGym fitness split rows via HF datasets-server."""

    out = CACHE_ROOT / "rnagym" / "fitness_sample.json"
    source = (
        "https://datasets-server.huggingface.co/rows?"
        + urlencode(
            {
                "dataset": "Marks-lab/RNAgym",
                "config": "default",
                "split": "fitness",
                "offset": "0",
                "length": str(n),
            }
        )
    )
    if out.exists() and not force:
        data = json.loads(out.read_text(encoding="utf-8"))
        receipt = DatasetFetchReceipt(
            dataset_id="rnagym",
            source=source,
            transport="huggingface-datasets-server",
            local_path=str(out.relative_to(ROOT)),
            n_rows=len(data.get("rows", [])),
            fetched_at=str(data.get("fetched_at", "")),
            epistemic_status="CACHED_ONLINE_SAMPLE",
            license_note="RNAGym (Marks-lab/RNAgym); check upstream license before redistribution",
            provenance=dict(data.get("provenance") or {}),
            detail="cache hit",
        )
        _update_manifest(receipt)
        return receipt

    payload = _http_get_json(source)
    rows = [item["row"] for item in payload.get("rows", [])]
    # Truncate long sequences in cache for repo hygiene; keep full in episode build from rows.
    fetched_at = datetime.now(timezone.utc).isoformat()
    envelope = {
        "dataset_id": "rnagym",
        "hf_dataset": "Marks-lab/RNAgym",
        "config": "default",
        "split": "fitness",
        "fetched_at": fetched_at,
        "source": source,
        "provenance": {"api": "huggingface datasets-server"},
        "rows": rows,
    }
    _write_json(out, envelope)
    receipt = DatasetFetchReceipt(
        dataset_id="rnagym",
        source=source,
        transport="huggingface-datasets-server",
        local_path=str(out.relative_to(ROOT)),
        n_rows=len(rows),
        fetched_at=fetched_at,
        epistemic_status="DOWNLOADED_ONLINE_SAMPLE",
        license_note="RNAGym (Marks-lab/RNAgym); check upstream license before redistribution",
        provenance=envelope["provenance"],
    )
    _update_manifest(receipt)
    return receipt


def fetch_clinvar_sample(*, n: int = 3, force: bool = False) -> DatasetFetchReceipt:
    """Fetch ClinVar pathogenic BRCA1 variants via NCBI E-utilities (online service)."""

    out = CACHE_ROOT / "clinvar" / "brca1_pathogenic_sample.json"
    search_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        + urlencode(
            {
                "db": "clinvar",
                "term": "BRCA1[gene] AND pathogenic[clinical_significance]",
                "retmax": str(n),
                "retmode": "json",
            }
        )
    )
    if out.exists() and not force:
        data = json.loads(out.read_text(encoding="utf-8"))
        receipt = DatasetFetchReceipt(
            dataset_id="clinvar",
            source=search_url,
            transport="ncbi-eutils",
            local_path=str(out.relative_to(ROOT)),
            n_rows=len(data.get("rows", [])),
            fetched_at=str(data.get("fetched_at", "")),
            epistemic_status="CACHED_ONLINE_SAMPLE",
            license_note="NCBI ClinVar public data; cite ClinVar",
            provenance=dict(data.get("provenance") or {}),
            detail="cache hit",
        )
        _update_manifest(receipt)
        return receipt

    search = _http_get_json(search_url)
    ids = search.get("esearchresult", {}).get("idlist", [])
    summary_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
        + urlencode({"db": "clinvar", "id": ",".join(ids), "retmode": "json"})
    )
    summary = _http_get_json(summary_url)
    rows = []
    for uid in summary.get("result", {}).get("uids", []):
        row = dict(summary["result"][uid])
        row["uid"] = uid
        rows.append(row)
    fetched_at = datetime.now(timezone.utc).isoformat()
    envelope = {
        "dataset_id": "clinvar",
        "fetched_at": fetched_at,
        "source_search": search_url,
        "source_summary": summary_url,
        "provenance": {"api": "NCBI E-utilities", "query": "BRCA1 pathogenic"},
        "rows": rows,
    }
    _write_json(out, envelope)
    receipt = DatasetFetchReceipt(
        dataset_id="clinvar",
        source=search_url,
        transport="ncbi-eutils",
        local_path=str(out.relative_to(ROOT)),
        n_rows=len(rows),
        fetched_at=fetched_at,
        epistemic_status="DOWNLOADED_ONLINE_SAMPLE",
        license_note="NCBI ClinVar public data; cite ClinVar",
        provenance=envelope["provenance"],
    )
    _update_manifest(receipt)
    return receipt


def fetch_proteingym_reference_sample(*, n: int = 3, force: bool = False) -> DatasetFetchReceipt:
    """Download ProteinGym substitution reference CSV (small) from Hugging Face."""

    out = CACHE_ROOT / "proteingym" / "reference_substitutions_sample.json"
    source = (
        "https://huggingface.co/datasets/ICML2022/ProteinGym/resolve/main/"
        "ProteinGym_reference_file_substitutions.csv"
    )
    if out.exists() and not force:
        data = json.loads(out.read_text(encoding="utf-8"))
        receipt = DatasetFetchReceipt(
            dataset_id="proteingym",
            source=source,
            transport="huggingface-resolve",
            local_path=str(out.relative_to(ROOT)),
            n_rows=len(data.get("rows", [])),
            fetched_at=str(data.get("fetched_at", "")),
            epistemic_status="CACHED_ONLINE_SAMPLE",
            license_note="ProteinGym reference metadata; DMS assay tables not fully mirrored",
            provenance=dict(data.get("provenance") or {}),
            detail="cache hit",
        )
        _update_manifest(receipt)
        return receipt

    text = _http_get_text(source)
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for i, row in enumerate(reader):
        if i >= n:
            break
        # Keep a short sequence prefix for episode construction.
        seq = row.get("target_seq") or ""
        rows.append(
            {
                "DMS_id": row.get("DMS_id"),
                "UniProt_ID": row.get("UniProt_ID"),
                "taxon": row.get("taxon"),
                "seq_len": row.get("seq_len"),
                "molecule_name": row.get("molecule_name"),
                "source_organism": row.get("source_organism"),
                "selection_assay": row.get("selection_assay"),
                "target_seq_prefix": seq[:80],
                "target_seq_len": len(seq),
            }
        )
    fetched_at = datetime.now(timezone.utc).isoformat()
    envelope = {
        "dataset_id": "proteingym",
        "fetched_at": fetched_at,
        "source": source,
        "provenance": {
            "api": "huggingface resolve",
            "file": "ProteinGym_reference_file_substitutions.csv",
            "note": "reference metadata sample; full DMS CSVs not downloaded",
        },
        "rows": rows,
    }
    _write_json(out, envelope)
    receipt = DatasetFetchReceipt(
        dataset_id="proteingym",
        source=source,
        transport="huggingface-resolve",
        local_path=str(out.relative_to(ROOT)),
        n_rows=len(rows),
        fetched_at=fetched_at,
        epistemic_status="DOWNLOADED_ONLINE_SAMPLE",
        license_note="ProteinGym reference metadata; DMS assay tables not fully mirrored",
        provenance=envelope["provenance"],
    )
    _update_manifest(receipt)
    return receipt


def fetch_opengenome2_style_ncbi_sample(*, force: bool = False) -> DatasetFetchReceipt:
    """Online genomic context for OpenGenome2 benchmark family via NCBI nucleotide.

    Full OpenGenome2 FASTA shards are multi-GB; we do not mirror them. NCBI
    provides held-out genomic sequence returns for sequence-likelihood /
    gene-completion under the same benchmark families.
    """

    out = CACHE_ROOT / "opengenome2" / "ncbi_genomic_context_sample.json"
    # E. coli K-12 window + a short human promoter-like NCBI record.
    queries = [
        {"id": "NC_000913.3", "start": 1, "stop": 160, "label": "ecoli_k12_window"},
        {"id": "NC_000913.3", "start": 2000, "stop": 2160, "label": "ecoli_k12_interior"},
    ]
    source = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    if out.exists() and not force:
        data = json.loads(out.read_text(encoding="utf-8"))
        receipt = DatasetFetchReceipt(
            dataset_id="opengenome2",
            source=source,
            transport="ncbi-eutils-stand-in-for-opengenome2-family",
            local_path=str(out.relative_to(ROOT)),
            n_rows=len(data.get("rows", [])),
            fetched_at=str(data.get("fetched_at", "")),
            epistemic_status="CACHED_ONLINE_STAND_IN",
            license_note=(
                "NCBI nucleotide public sequence; OpenGenome2 corpus itself not mirrored "
                "(Arc Institute / HF shards are multi-GB)"
            ),
            provenance=dict(data.get("provenance") or {}),
            detail="cache hit",
        )
        _update_manifest(receipt)
        return receipt

    rows = []
    for q in queries:
        url = (
            source
            + "?"
            + urlencode(
                {
                    "db": "nucleotide",
                    "id": q["id"],
                    "rettype": "fasta",
                    "retmode": "text",
                    "seq_start": str(q["start"]),
                    "seq_stop": str(q["stop"]),
                }
            )
        )
        fasta = _http_get_text(url)
        lines = [ln.strip() for ln in fasta.splitlines() if ln.strip()]
        header = lines[0] if lines else ""
        seq = "".join(ln for ln in lines[1:] if not ln.startswith(">"))
        rows.append(
            {
                "label": q["label"],
                "accession": q["id"],
                "start": q["start"],
                "stop": q["stop"],
                "header": header,
                "sequence": seq,
                "source_url": url,
            }
        )
    # Also pin OpenGenome2 README for architecture provenance.
    readme_url = (
        "https://huggingface.co/datasets/arcinstitute/opengenome2/resolve/main/README.md"
    )
    try:
        readme = _http_get_text(readme_url)[:2000]
    except (HTTPError, URLError, TimeoutError, OSError):
        readme = ""
    fetched_at = datetime.now(timezone.utc).isoformat()
    envelope = {
        "dataset_id": "opengenome2",
        "fetched_at": fetched_at,
        "opengenome2_hf": "https://huggingface.co/datasets/arcinstitute/opengenome2",
        "opengenome2_readme_excerpt": readme,
        "provenance": {
            "api": "NCBI E-utilities efetch",
            "role": (
                "online genomic context stand-in for OpenGenome2 benchmark families; "
                "full Arc OpenGenome2 corpus not downloaded"
            ),
            "benchmark_families": ["sequence-likelihood", "gene-completion"],
        },
        "rows": rows,
    }
    _write_json(out, envelope)
    receipt = DatasetFetchReceipt(
        dataset_id="opengenome2",
        source=source,
        transport="ncbi-eutils-stand-in-for-opengenome2-family",
        local_path=str(out.relative_to(ROOT)),
        n_rows=len(rows),
        fetched_at=fetched_at,
        epistemic_status="DOWNLOADED_ONLINE_STAND_IN",
        license_note=(
            "NCBI nucleotide public sequence; OpenGenome2 corpus itself not mirrored"
        ),
        provenance=envelope["provenance"],
    )
    _update_manifest(receipt)
    return receipt


def fetch_all_open_samples(*, force: bool = False, n: int = 3) -> list[DatasetFetchReceipt]:
    """Fetch all currently wired online samples."""

    return [
        fetch_traitgym_sample(n=n, force=force),
        fetch_rnagym_sample(n=n, force=force),
        fetch_clinvar_sample(n=n, force=force),
        fetch_proteingym_reference_sample(n=n, force=force),
        fetch_opengenome2_style_ncbi_sample(force=force),
    ]


def _episode(
    *,
    episode_id: str,
    benchmark_id: str,
    shared_relation: str,
    modalities: dict[str, dict[str, Any]],
    source_observation: dict[str, Any],
    returned_observation: dict[str, Any],
    legal_actions: tuple[dict[str, Any], ...],
    openings: tuple[str, ...] = (),
    axiometric_shadows: dict[str, Any] | None = None,
    dataset_id: str,
) -> ReturnUnifiedEpisodeSpec:
    biological = BiologicalEpisode(
        modalities=modalities,
        shared_relation=shared_relation,
        openings=openings or ("next-return-layer",),
        axiometric_shadows=dict(axiometric_shadows or {}),
    )
    biological.validate()
    return ReturnUnifiedEpisodeSpec(
        episode_id=episode_id,
        benchmark_id=benchmark_id,
        biological=biological,
        source_observation=source_observation,
        legal_actions=legal_actions,
        returned_observation=returned_observation,
        next_legal_actions=({"act": "observe"},),
        independent=True,
        contradictory=False,
        self_authored=False,
        role=f"open-dataset:{dataset_id}",
    )


def episodes_from_traitgym(path: Path | None = None) -> list[ReturnUnifiedEpisodeSpec]:
    target = path or (CACHE_ROOT / "traitgym" / "mendelian_traits_test_sample.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    episodes = []
    for i, row in enumerate(data.get("rows", [])):
        chrom = row.get("chrom")
        pos = row.get("pos")
        ref = row.get("ref")
        alt = row.get("alt")
        label = bool(row.get("label"))
        consequence = row.get("consequence")
        variant = f"{chrom}:{pos}:{ref}>{alt}"
        episodes.append(
            _episode(
                episode_id=f"traitgym-{i:03d}",
                benchmark_id="variant-effect",
                shared_relation="traitgym-variant-return",
                modalities={
                    "DNA": {
                        "variant": variant,
                        "chrom": chrom,
                        "pos": pos,
                        "ref": ref,
                        "alt": alt,
                        "dataset": "traitgym",
                    },
                    "environment": {"cohort": "traitgym-mendelian_traits-test"},
                    "returned_consequence": {
                        "label": label,
                        "consequence": consequence,
                        "measured": True,
                        "dataset": "traitgym",
                    },
                },
                source_observation={"variant": variant, "phase": "pre-return"},
                returned_observation={
                    "variant": variant,
                    "label": label,
                    "consequence": consequence,
                    "measured": True,
                },
                legal_actions=({"act": "score_variant"}, {"act": "hold"}),
                openings=("tissue-context-layer",),
                axiometric_shadows={"pip": row.get("pip"), "label_bool": label},
                dataset_id="traitgym",
            )
        )
    return episodes


def episodes_from_rnagym(path: Path | None = None) -> list[ReturnUnifiedEpisodeSpec]:
    target = path or (CACHE_ROOT / "rnagym" / "fitness_sample.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    episodes = []
    for i, row in enumerate(data.get("rows", [])):
        seq = str(row.get("sequence") or "")
        seq_short = seq[:120]
        score = row.get("dms_score")
        mutant = row.get("mutant")
        episodes.append(
            _episode(
                episode_id=f"rnagym-{i:03d}",
                benchmark_id="rna-fitness",
                shared_relation="rnagym-fitness-return",
                modalities={
                    "RNA": {
                        "sequence_prefix": seq_short,
                        "sequence_len": len(seq),
                        "mutant": mutant,
                        "dataset": "rnagym",
                    },
                    "environment": {"assay": "rnagym-fitness"},
                    "returned_consequence": {
                        "dms_score": score,
                        "measured": True,
                        "dataset": "rnagym",
                    },
                },
                source_observation={"mutant": mutant, "phase": "pre-return"},
                returned_observation={
                    "mutant": mutant,
                    "dms_score": score,
                    "measured": True,
                },
                legal_actions=({"act": "score_rna_fitness"}, {"act": "hold"}),
                openings=("ligand-bound-layer",),
                axiometric_shadows={"dms_score": score},
                dataset_id="rnagym",
            )
        )
    return episodes


def episodes_from_clinvar(path: Path | None = None) -> list[ReturnUnifiedEpisodeSpec]:
    target = path or (CACHE_ROOT / "clinvar" / "brca1_pathogenic_sample.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    episodes = []
    for i, row in enumerate(data.get("rows", [])):
        accession = row.get("accession") or row.get("uid")
        title = row.get("title") or ""
        obj_type = row.get("obj_type")
        # Best-effort cdna / protein change from variation_set
        cdna = None
        locs = []
        for vs in row.get("variation_set") or []:
            cdna = cdna or vs.get("cdna_change") or vs.get("variation_name")
            for loc in vs.get("variation_loc") or []:
                if loc.get("status") == "current":
                    locs.append(
                        {
                            "chr": loc.get("chr"),
                            "start": loc.get("start"),
                            "stop": loc.get("stop"),
                            "assembly": loc.get("assembly_name"),
                        }
                    )
        episodes.append(
            _episode(
                episode_id=f"clinvar-{i:03d}",
                benchmark_id="variant-effect",
                shared_relation="clinvar-clinical-return",
                modalities={
                    "DNA": {
                        "accession": accession,
                        "title": title,
                        "obj_type": obj_type,
                        "cdna_change": cdna,
                        "locations": locs,
                        "gene": "BRCA1",
                        "dataset": "clinvar",
                    },
                    "environment": {"clinvar_query": "BRCA1 pathogenic"},
                    "returned_consequence": {
                        "clinical_significance": "pathogenic",
                        "accession": accession,
                        "measured": True,
                        "dataset": "clinvar",
                    },
                },
                source_observation={"accession": accession, "phase": "pre-return"},
                returned_observation={
                    "accession": accession,
                    "clinical_significance": "pathogenic",
                    "title": title,
                    "measured": True,
                },
                legal_actions=({"act": "interpret_variant"}, {"act": "hold"}),
                openings=("clinical-context-layer",),
                axiometric_shadows={"uid": row.get("uid")},
                dataset_id="clinvar",
            )
        )
    return episodes


def episodes_from_proteingym(path: Path | None = None) -> list[ReturnUnifiedEpisodeSpec]:
    target = path or (CACHE_ROOT / "proteingym" / "reference_substitutions_sample.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    episodes = []
    for i, row in enumerate(data.get("rows", [])):
        dms_id = row.get("DMS_id")
        prefix = row.get("target_seq_prefix") or ""
        episodes.append(
            _episode(
                episode_id=f"proteingym-{i:03d}",
                benchmark_id="variant-effect",
                shared_relation="proteingym-dms-reference-return",
                modalities={
                    "protein": {
                        "DMS_id": dms_id,
                        "UniProt_ID": row.get("UniProt_ID"),
                        "molecule_name": row.get("molecule_name"),
                        "seq_prefix": prefix,
                        "seq_len": row.get("target_seq_len") or row.get("seq_len"),
                        "dataset": "proteingym",
                    },
                    "environment": {
                        "organism": row.get("source_organism"),
                        "assay": row.get("selection_assay"),
                        "taxon": row.get("taxon"),
                    },
                    "returned_consequence": {
                        "reference_assay_present": True,
                        "DMS_id": dms_id,
                        "measured": True,
                        "dataset": "proteingym",
                        "note": "reference metadata return; full DMS table not required for admission",
                    },
                },
                source_observation={"DMS_id": dms_id, "phase": "pre-return"},
                returned_observation={
                    "DMS_id": dms_id,
                    "reference_assay_present": True,
                    "measured": True,
                },
                legal_actions=({"act": "score_protein_dms"}, {"act": "hold"}),
                openings=("dms-table-layer",),
                axiometric_shadows={"seq_len": row.get("seq_len")},
                dataset_id="proteingym",
            )
        )
    return episodes


def episodes_from_opengenome2_style(path: Path | None = None) -> list[ReturnUnifiedEpisodeSpec]:
    target = path or (CACHE_ROOT / "opengenome2" / "ncbi_genomic_context_sample.json")
    data = json.loads(target.read_text(encoding="utf-8"))
    episodes = []
    for i, row in enumerate(data.get("rows", [])):
        seq = str(row.get("sequence") or "")
        if len(seq) < 40:
            continue
        # sequence-likelihood episode
        episodes.append(
            _episode(
                episode_id=f"opengenome2-seq-{i:03d}",
                benchmark_id="sequence-likelihood",
                shared_relation="opengenome2-family-genomic-context-return",
                modalities={
                    "DNA": {
                        "sequence": seq,
                        "accession": row.get("accession"),
                        "label": row.get("label"),
                        "dataset": "opengenome2-family-ncbi-stand-in",
                    },
                    "environment": {"source": "ncbi-nucleotide", "milieu": "genomic-context"},
                    "returned_consequence": {
                        "viability": "sequence_observed",
                        "measured": True,
                        "dataset": "opengenome2-family-ncbi-stand-in",
                    },
                },
                source_observation={
                    "accession": row.get("accession"),
                    "start": row.get("start"),
                    "stop": row.get("stop"),
                    "phase": "pre-return",
                },
                returned_observation={
                    "sequence": seq,
                    "measured": True,
                    "accession": row.get("accession"),
                },
                legal_actions=({"act": "score_context"}, {"act": "hold"}),
                openings=("next-locus-layer",),
                axiometric_shadows={"length": len(seq)},
                dataset_id="opengenome2",
            )
        )
        # gene-completion: mask interior span, return completed bases
        mask_start = 20
        mask_len = 12
        prefix = seq[:mask_start]
        completed = seq[mask_start : mask_start + mask_len]
        suffix = seq[mask_start + mask_len :]
        episodes.append(
            _episode(
                episode_id=f"opengenome2-gene-{i:03d}",
                benchmark_id="gene-completion",
                shared_relation="opengenome2-family-gene-completion-return",
                modalities={
                    "DNA": {
                        "prefix": prefix,
                        "mask_span": mask_len,
                        "accession": row.get("accession"),
                        "dataset": "opengenome2-family-ncbi-stand-in",
                    },
                    "RNA": {"transcript_hint": "genomic_window"},
                    "returned_consequence": {
                        "completed_span": completed,
                        "suffix_len": len(suffix),
                        "measured": True,
                        "dataset": "opengenome2-family-ncbi-stand-in",
                    },
                },
                source_observation={"prefix": prefix, "mask_span": mask_len},
                returned_observation={
                    "prefix": prefix,
                    "completed_span": completed,
                    "measured": True,
                },
                legal_actions=({"act": "complete_span"}, {"act": "abstain"}),
                openings=("expression-layer",),
                axiometric_shadows={"mask_len": mask_len},
                dataset_id="opengenome2",
            )
        )
    return episodes


def load_all_open_episodes() -> list[ReturnUnifiedEpisodeSpec]:
    """Load cached open-dataset episodes (empty list if cache missing)."""

    loaders = [
        (CACHE_ROOT / "traitgym" / "mendelian_traits_test_sample.json", episodes_from_traitgym),
        (CACHE_ROOT / "rnagym" / "fitness_sample.json", episodes_from_rnagym),
        (CACHE_ROOT / "clinvar" / "brca1_pathogenic_sample.json", episodes_from_clinvar),
        (
            CACHE_ROOT / "proteingym" / "reference_substitutions_sample.json",
            episodes_from_proteingym,
        ),
        (
            CACHE_ROOT / "opengenome2" / "ncbi_genomic_context_sample.json",
            episodes_from_opengenome2_style,
        ),
    ]
    episodes: list[ReturnUnifiedEpisodeSpec] = []
    for path, loader in loaders:
        if path.exists():
            episodes.extend(loader(path))
    return episodes


def open_dataset_cache_availability() -> dict[str, dict[str, Any]]:
    """Availability including downloaded online samples under data_cache/."""

    mapping = {
        "traitgym": CACHE_ROOT / "traitgym" / "mendelian_traits_test_sample.json",
        "rnagym": CACHE_ROOT / "rnagym" / "fitness_sample.json",
        "clinvar": CACHE_ROOT / "clinvar" / "brca1_pathogenic_sample.json",
        "proteingym": CACHE_ROOT / "proteingym" / "reference_substitutions_sample.json",
        "opengenome2": CACHE_ROOT / "opengenome2" / "ncbi_genomic_context_sample.json",
    }
    manifest = load_cache_manifest().get("datasets", {})
    out: dict[str, dict[str, Any]] = {}
    for dataset_id, path in mapping.items():
        meta = manifest.get(dataset_id, {})
        local_path: str | None
        try:
            local_path = str(path.relative_to(ROOT)) if path.exists() else None
        except ValueError:
            local_path = str(path) if path.exists() else None
        out[dataset_id] = {
            "local_present": path.exists(),
            "local_path": local_path,
            "epistemic_status": meta.get("epistemic_status"),
            "transport": meta.get("transport"),
            "n_rows": meta.get("n_rows"),
            "fetched_at": meta.get("fetched_at"),
        }
    return out


def receipt_to_dict(receipt: DatasetFetchReceipt) -> dict[str, Any]:
    return {
        "dataset_id": receipt.dataset_id,
        "source": receipt.source,
        "transport": receipt.transport,
        "local_path": receipt.local_path,
        "n_rows": receipt.n_rows,
        "fetched_at": receipt.fetched_at,
        "epistemic_status": receipt.epistemic_status,
        "license_note": receipt.license_note,
        "provenance": receipt.provenance,
        "ok": receipt.ok,
        "detail": receipt.detail,
        "digest": digest(
            {
                "dataset": receipt.dataset_id,
                "path": receipt.local_path,
                "n": receipt.n_rows,
                "at": receipt.fetched_at,
            }
        ),
    }


__all__ = [
    "CACHE_ROOT",
    "DatasetFetchReceipt",
    "episodes_from_clinvar",
    "episodes_from_opengenome2_style",
    "episodes_from_proteingym",
    "episodes_from_rnagym",
    "episodes_from_traitgym",
    "fetch_all_open_samples",
    "fetch_clinvar_sample",
    "fetch_opengenome2_style_ncbi_sample",
    "fetch_proteingym_reference_sample",
    "fetch_rnagym_sample",
    "fetch_traitgym_sample",
    "load_all_open_episodes",
    "load_cache_manifest",
    "open_dataset_cache_availability",
    "receipt_to_dict",
]
