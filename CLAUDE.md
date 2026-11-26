# Nonux

Distribuzione Linux derivata da Chimera, senza `/usr` e con una sola cartella
per ogni tipo di file. Piano di lavoro: `docs/fase-0-piano.md`.

## Layout: regole che non si discutono

La specifica normativa è `docs/hier.md` (forma leggibile dagli strumenti:
`docs/hier.toml`). In breve:

- Prefisso di installazione `/`. Eseguibili in `/bin`, librerie in `/lib`,
  header in `/include`, dati in `/share`, configurazioni in `/etc`.
- Eseguibili interni di un pacchetto in `/lib/<pacchetto>/`.
- Servizi dinit e default dei pacchetti (`tmpfiles.d`, `sysusers.d`,
  `sysctl.d`, `modprobe.d`, `modules-load.d`, `binfmt.d`) solo in `/etc`: mai
  una cartella di default in `/lib` con override in `/etc` (D-18).
- Vietati: `/usr`, `/usr/local`, `/sbin`, `/lib64`, `/lib32`, `/libexec`,
  `/opt`, `/media`, `/srv`, `/var/run`, `/var/lock`, `/var/tmp`.
- **Mai aggiungere symlink di compatibilità** verso i percorsi vietati, nemmeno
  come soluzione temporanea. Se un programma li richiede, si corregge il
  programma.

Se si cambia il layout, vanno aggiornati insieme `hier.md`, `hier.toml` e
`man/hier.7`: lo verifica `tools/tests/test_hier.py`.

## Struttura

- `docs/` — specifica, decisioni, note tecniche.
- `cports/` — submodule: fork di `chimera-linux/cports`, branch `nonux`.
  Le modifiche al sistema di build e ai pacchetti si fanno lì.
- `services/` (da creare in fase 2) — servizi dinit di avvio, nostri. Chiamano
  direttamente i programmi; uno script shell è ammesso solo come eccezione
  documentata (D-18b). `dinit-chimera` non si modifica.
- `tools/usr-inventory/` — inventario dei riferimenti a `/usr` in cports.
- `tools/tests/` — test della specifica.

Le cartelle previste dal piano e non ancora create (`tools/path-audit/`,
`tools/shebang-fix/`, `etc-template/`, `image/`, `ci/`) si
aggiungono quando hanno un contenuto.

## Comandi

```
python3 -m pytest -q tools                 # test
ruff check tools                           # lint
mandoc -Tlint -Wwarning docs/man/hier.7    # pagina man
tools/usr-inventory/usr_inventory.py cports \
    --packages tools/usr-inventory/minimal.txt   # inventario di /usr
```

Build di un pacchetto con il layout senza `/usr` (da utente non root, vedi
`docs/prova-fattibilita.md`):

```
cd cports && CBUILD_TARGET_PREFIX=/ ./cbuild -r packages-nonux pkg main/<nome>
```

## Convenzioni

- Documentazione e messaggi di commit in italiano.
- Decisioni architetturali: si registrano in `docs/decisioni.md` con
  motivazione, mai solo nel codice.
- Patch ai sorgenti dei pacchetti: una patch per problema, con un'intestazione
  che spiega perché serve e se è proponibile upstream.
- Modifiche a cports: piccole e separate dai cambi di versione, per ridurre i
  conflitti a ogni sincronizzazione con Chimera.
- `docs/nota-cports-cbuild.md` è generato: si rigenera, non si modifica a mano.
