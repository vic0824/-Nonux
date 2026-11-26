import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import usr_inventory as ui


def make_tree(root):
    def w(rel, text):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    w("src/cbuild/util/meson.py", '# /usr in un commento\nargs = ["--prefix=/usr"]\n')
    w("src/cbuild/core/template.py", 'self.install_file(src, "usr/bin")\n')
    w(
        "main/foo/template.py",
        'configure_args = ["--with-x=/usr"]\n'
        'self.take("usr/bin/foo")\n'
        'env = {"X": "/usr/lib/foo"}\n'
        'user = "nobody"  # non è un percorso\n'
        'pkgname = "libusrsctp"\n',
    )
    w("main/foo/patches/a.patch", "--- a/usr/x\n+++ b/usr/x\n-old /usr/a\n+new /usr/b\n")
    w("main/foo/files/foo.service", "command = /usr/bin/foo\n")
    w("main/clean/template.py", 'pkgname = "clean"\n')
    (root / "main/foo-devel").symlink_to("foo")


def test_classification(tmp_path):
    make_tree(tmp_path)
    hits = list(ui.scan(tmp_path))
    got = sorted((h.cat, h.path, h.line) for h in hits)
    assert got == [
        ("A", "src/cbuild/util/meson.py", 2),
        ("B", "src/cbuild/core/template.py", 1),
        ("C", "main/foo/template.py", 2),
        ("D1", "main/foo/template.py", 1),
        ("D2", "main/foo/template.py", 3),
        ("E", "main/foo/patches/a.patch", 4),
        ("G", "main/foo/files/foo.service", 1),
    ]


def test_symlinked_subpackages_are_not_counted(tmp_path):
    make_tree(tmp_path)
    assert ui.count_packages(tmp_path) == {"main": 2}


def test_cli_outputs(tmp_path):
    make_tree(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    pk = out / "pk.txt"
    pk.write_text("# commento\nmain/foo\nmain/clean\nmain/missing\n")
    rc = ui.main(
        [
            str(tmp_path),
            "--csv", str(out / "i.csv"),
            "--md", str(out / "i.md"),
            "--core-md", str(out / "c.md"),
            "--packages", str(pk),
        ]
    )
    assert rc == 0
    rows = list(csv.DictReader((out / "i.csv").open()))
    assert len(rows) == 7
    md = (out / "i.md").read_text()
    assert "| main/foo | 1 | 1 | 1 | 1 | 1 | 5 |" in md
    assert "| main/clean | | | | | | 0 |" in md
    assert "| main/missing | | | | | | assente |" in md
    core = (out / "c.md").read_text()
    assert "`src/cbuild/util/meson.py:2`" in core
