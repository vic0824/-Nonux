"""Coerenza tra docs/hier.toml, docs/hier.md e docs/man/hier.7."""

import pathlib
import re

import tomllib

DOCS = pathlib.Path(__file__).resolve().parents[2] / "docs"
SPEC = tomllib.loads((DOCS / "hier.toml").read_text())
MD = (DOCS / "hier.md").read_text()
MAN = (DOCS / "man" / "hier.7").read_text()

ALLOWED = {d["path"] for d in SPEC["dir"]}
FORBIDDEN = {f["path"] for f in SPEC["forbidden"]}


def md_table_paths(heading):
    """Prima colonna della tabella sotto il titolo dato, solo voci di radice."""
    section = MD.split(f"## {heading}", 1)[1].split("\n## ", 1)[0]
    cells = re.findall(r"^\| `(/[^`]*)` \|", section, flags=re.MULTILINE)
    return set(cells)


def test_allowed_and_forbidden_are_disjoint():
    assert not ALLOWED & FORBIDDEN


def test_allowed_are_top_level():
    for p in ALLOWED:
        assert re.fullmatch(r"/[a-z]+", p), p


def test_no_allowed_dir_is_under_a_forbidden_one():
    for p in ALLOWED:
        assert not any(p.startswith(f + "/") for f in FORBIDDEN), p


def test_replacements_point_to_allowed_dirs():
    for f in SPEC["forbidden"]:
        top = "/" + f["use"].strip("/").split("/")[0] if f["use"] != "/" else "/"
        assert top == "/" or top in ALLOWED, f


def test_build_dirs_are_inside_allowed_dirs():
    build = dict(SPEC["build"])
    assert build.pop("prefix") == "/"
    values = build.pop("pkgconfigdirs") + list(build.values())
    for v in values:
        assert "/" + v.split("/")[1] in ALLOWED, v
        assert not any(v == f or v.startswith(f + "/") for f in FORBIDDEN), v


def test_build_vars_are_declared_by_a_dir():
    declared = {v for d in SPEC["dir"] for v in d.get("vars", [])}
    assert declared == set(SPEC["build"]) - {"prefix", "pkgconfigdirs"}


def test_markdown_allowed_table_matches_toml():
    paths = {p for p in md_table_paths("Cartelle ammesse") if p.count("/") == 1}
    assert paths == ALLOWED


def test_markdown_forbidden_table_matches_toml():
    assert md_table_paths("Percorsi vietati") == FORBIDDEN


def test_man_page_mentions_every_path():
    for p in ALLOWED | FORBIDDEN:
        assert re.search(rf"Pa .*{re.escape(p)}\b", MAN), p
