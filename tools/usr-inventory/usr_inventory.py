#!/usr/bin/env python3
"""Inventario dei riferimenti a /usr in un checkout di cports.

Uso:
    usr_inventory.py CPORTS_DIR [--csv FILE] [--md FILE]
                     [--core-md FILE] [--packages FILE]

Scansiona cbuild, i template e i file che li accompagnano (patch, files/),
classifica ogni riga che cita `usr` e produce un CSV completo, un riepilogo
in Markdown e l'elenco file:riga dei punti in cbuild.

Categorie:
    A   cbuild: build style, util, hook, profili (da rendere parametrico)
    B   cbuild: helper dei template in core/template.py
    C   template: percorso letterale relativo al destdir ("usr/bin/foo")
    D1  template: argomento di configurazione (--foo=/usr..., -DFOO=/usr...)
    D2  template: percorso assoluto in altra logica (env, sed, symlink, ...)
    E   patch: righe aggiunte che contengono /usr
    G   file ausiliari del pacchetto (files/, script, servizi)
"""

import argparse
import collections
import csv
import pathlib
import re
import sys

# `usr` come componente di percorso: "/usr", "usr/...", oppure la stringa "usr"
USR = re.compile(r"""(?<![\w.-])/?usr/|(?<![\w.-])/usr\b|["']usr["']""")
REL_LITERAL = re.compile(r"""["']usr(/|["'])""")
CFG_ARG = re.compile(r"""=\s*/?usr\b|=\{?[\w.]*\}?/usr\b""")

REPOS = ("main", "user")

DESCR = {
    "A": "cbuild: build style, util, hook, profili",
    "B": "cbuild: helper dei template (core/template.py)",
    "C": "template: percorso letterale relativo al destdir",
    "D1": "template: argomento di configurazione",
    "D2": "template: percorso assoluto in altra logica",
    "E": "patch: righe aggiunte con /usr",
    "G": "file ausiliari del pacchetto",
}

Hit = collections.namedtuple("Hit", "cat pkg path line text")


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return []


def classify_template_line(text):
    if REL_LITERAL.search(text):
        return "C"
    if CFG_ARG.search(text):
        return "D1"
    return "D2"


def scan_python(path, rel, pkg, catfn):
    for n, text in enumerate(read_lines(path), 1):
        s = text.strip()
        if not s or s.startswith("#") or not USR.search(s):
            continue
        yield Hit(catfn(s), pkg, rel, n, s)


def scan_plain(path, rel, pkg, cat, added_only=False):
    for n, text in enumerate(read_lines(path), 1):
        if added_only and (not text.startswith("+") or text.startswith("+++")):
            continue
        if USR.search(text):
            yield Hit(cat, pkg, rel, n, text.strip())


def scan(root):
    cb = root / "src" / "cbuild"
    for p in sorted(cb.rglob("*.py")):
        rel = p.relative_to(root).as_posix()
        cat = "B" if rel.endswith("core/template.py") else "A"
        yield from scan_python(p, rel, "", lambda _s, c=cat: c)

    for repo in REPOS:
        base = root / repo
        if not base.is_dir():
            continue
        for d in sorted(base.iterdir()):
            # i sottopacchetti sono symlink alla cartella del principale
            if d.is_symlink() or not d.is_dir():
                continue
            pkg = f"{repo}/{d.name}"
            for p in sorted(d.rglob("*")):
                if not p.is_file() or p.is_symlink():
                    continue
                rel = p.relative_to(root).as_posix()
                if p.name == "template.py" and p.parent == d:
                    yield from scan_python(p, rel, pkg, classify_template_line)
                elif "patches" in p.relative_to(d).parts:
                    yield from scan_plain(p, rel, pkg, "E", added_only=True)
                elif p.name != "update.py":
                    yield from scan_plain(p, rel, pkg, "G")


def count_packages(root):
    n = {}
    for repo in REPOS:
        base = root / repo
        if base.is_dir():
            n[repo] = sum(
                1 for d in base.iterdir() if d.is_dir() and not d.is_symlink()
            )
    return n


def summary_md(hits, totals, wanted):
    out = ["## Riepilogo per categoria", ""]
    out += ["| Cat. | Descrizione | Righe | File | Pacchetti |", "|---|---|---:|---:|---:|"]
    for cat, descr in DESCR.items():
        hs = [h for h in hits if h.cat == cat]
        out.append(
            f"| {cat} | {descr} | {len(hs)} | {len({h.path for h in hs})} "
            f"| {len({h.pkg for h in hs if h.pkg}) or '—'} |"
        )
    out += ["", "## Pacchetti toccati", ""]
    out += ["| Repo | Template | Con almeno un riferimento | Solo categoria C |", "|---|---:|---:|---:|"]
    bypkg = collections.defaultdict(collections.Counter)
    for h in hits:
        if h.pkg:
            bypkg[h.pkg][h.cat] += 1
    for repo, tot in totals.items():
        mine = {p: c for p, c in bypkg.items() if p.startswith(repo + "/")}
        only_c = sum(1 for c in mine.values() if set(c) == {"C"})
        out.append(f"| {repo} | {tot} | {len(mine)} | {only_c} |")

    if wanted:
        out += ["", "## Pacchetti del sistema minimo", ""]
        out += ["| Pacchetto | C | D1 | D2 | E | G | Totale |", "|---|---:|---:|---:|---:|---:|---:|"]
        tot = collections.Counter()
        for name in wanted:
            c = bypkg.get(name)
            if c is None:
                state = "assente" if name not in ALL_PKGS else "0"
                out.append(f"| {name} | | | | | | {state} |")
                continue
            tot.update(c)
            out.append(
                f"| {name} | {c['C']} | {c['D1']} | {c['D2']} | {c['E']} "
                f"| {c['G']} | {sum(c.values())} |"
            )
        out.append(
            f"| **Totale** | {tot['C']} | {tot['D1']} | {tot['D2']} | {tot['E']} "
            f"| {tot['G']} | {sum(tot.values())} |"
        )

    out += ["", "## I 20 pacchetti con più riferimenti", ""]
    out += ["| Pacchetto | Righe |", "|---|---:|"]
    top = sorted(bypkg.items(), key=lambda kv: -sum(kv[1].values()))[:20]
    out += [f"| {p} | {sum(c.values())} |" for p, c in top]
    return "\n".join(out) + "\n"


def core_md(hits):
    out = ["| Cat. | File:riga | Testo |", "|---|---|---|"]
    for h in hits:
        if h.cat in ("A", "B"):
            text = h.text.replace("|", "\\|")
            out.append(f"| {h.cat} | `{h.path}:{h.line}` | `{text}` |")
    return "\n".join(out) + "\n"


ALL_PKGS = set()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cports", type=pathlib.Path)
    ap.add_argument("--csv", type=pathlib.Path)
    ap.add_argument("--md", type=pathlib.Path)
    ap.add_argument("--core-md", type=pathlib.Path)
    ap.add_argument("--packages", type=pathlib.Path, help="elenco pacchetti, uno per riga")
    args = ap.parse_args(argv)

    root = args.cports.resolve()
    if not (root / "src" / "cbuild").is_dir():
        ap.error(f"{root} non sembra un checkout di cports")

    hits = list(scan(root))
    totals = count_packages(root)
    for repo in totals:
        ALL_PKGS.update(
            f"{repo}/{d.name}"
            for d in (root / repo).iterdir()
            if d.is_dir() and not d.is_symlink()
        )

    wanted = []
    if args.packages:
        wanted = [
            ln.strip()
            for ln in args.packages.read_text().splitlines()
            if ln.strip() and not ln.startswith("#")
        ]

    if args.csv:
        with args.csv.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(Hit._fields)
            w.writerows(hits)
    md = summary_md(hits, totals, wanted)
    if args.md:
        args.md.write_text(md)
    else:
        sys.stdout.write(md)
    if args.core_md:
        args.core_md.write_text(core_md(hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
