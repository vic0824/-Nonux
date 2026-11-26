# hier — layout del filesystem di Nonux

Stato: bozza (fase 0, step 1). Questo documento è il riferimento normativo
per il layout. La stessa specifica esiste in forma leggibile dagli strumenti
in [`hier.toml`](hier.toml) e come pagina man in [`man/hier.7`](man/hier.7).

## Principi

1. Una sola cartella per ogni tipo di file (L-1).
2. Nessuna gerarchia `/usr` (L-2): il prefisso di installazione è `/`.
3. Nessun symlink di compatibilità verso i percorsi FHS (L-3).
4. Tutti gli eseguibili, di sistema e utente, in `/bin` (L-4).

## Cartelle ammesse

| Cartella | Contenuto | Note |
|----------|-----------|------|
| `/bin` | Tutti gli eseguibili destinati al `PATH` | Nessuna sottocartella |
| `/lib` | Librerie condivise e statiche, loader dinamico, moduli kernel (`/lib/modules`), firmware (`/lib/firmware`), file `pkgconfig` | |
| `/lib/<pacchetto>/` | Eseguibili interni non destinati al `PATH` (l'equivalente di `libexec`) | Decisione D-6 |
| `/include` | Header C/C++ | |
| `/share` | Dati indipendenti dall'architettura: man, locale, icone, font, dati dei pacchetti | |
| `/etc` | Configurazioni, compresi servizi dinit e default dei pacchetti (`dinit.d`, `tmpfiles.d`, `sysusers.d`, `sysctl.d`, `modprobe.d`, `modules-load.d`, `binfmt.d`) | Sotto git. Decisione D-18 |
| `/var` | Dati variabili persistenti: `log/`, `cache/`, `lib/` (stato dei servizi), `spool/` | |
| `/run` | Dati runtime | tmpfs |
| `/tmp` | File temporanei | tmpfs |
| `/home` | Home degli utenti | Dentro le home vale XDG (`~/.local/bin` ecc.) |
| `/root` | Home di root | |
| `/boot` | Kernel (UKI), ESP | Nessun initramfs (D-22) |
| `/mnt` | Unico punto per i mount manuali e automatici | |
| `/dev` | Filesystem virtuale del kernel | Non modificabile |
| `/proc` | Filesystem virtuale del kernel | Non modificabile |
| `/sys` | Filesystem virtuale del kernel | Non modificabile |
| `/src` | Sorgenti, incluso il kernel | Opzionale |

Qualsiasi altra voce nella radice è un errore.

## Percorsi vietati

Non devono esistere, nemmeno come symlink, e non devono comparire nei file
installati dai pacchetti (binari, script, file di dati).

| Percorso | Al suo posto |
|----------|--------------|
| `/usr` | `/` |
| `/usr/local` | `/` |
| `/sbin` | `/bin` |
| `/lib64` | `/lib` |
| `/lib32` | `/lib` |
| `/libexec` | `/lib/<pacchetto>` |
| `/opt` | `/` |
| `/media` | `/mnt` |
| `/srv` | `/var/lib/<servizio>` |
| `/var/run` | `/run` |
| `/var/lock` | `/run/lock` |
| `/var/tmp` | `/tmp` |

`/var/run` e `/var/lock` non sono nel piano originale: sono i due symlink di
compatibilità più diffusi e ricadono nella regola L-3. `/var/tmp` è vietata
perché la cartella temporanea è una sola (punto H-1).

## Variabili dei sistemi di build

Valori che il profilo di build deve passare a ogni pacchetto.

| Variabile | Valore | autotools | Meson | CMake (`GNUInstallDirs`) |
|-----------|--------|-----------|-------|--------------------------|
| `prefix` | `/` | `--prefix=` | `--prefix=/` | `CMAKE_INSTALL_PREFIX=/` |
| `bindir` | `/bin` | `--bindir` | `--bindir` | `CMAKE_INSTALL_BINDIR` |
| `sbindir` | `/bin` | `--sbindir` | `--sbindir` | `CMAKE_INSTALL_SBINDIR` |
| `libdir` | `/lib` | `--libdir` | `--libdir` | `CMAKE_INSTALL_LIBDIR` |
| `libexecdir` | `/lib` | `--libexecdir` | `--libexecdir` | `CMAKE_INSTALL_LIBEXECDIR` |
| `includedir` | `/include` | `--includedir` | `--includedir` | `CMAKE_INSTALL_INCLUDEDIR` |
| `datarootdir`, `datadir` | `/share` | `--datarootdir`, `--datadir` | `--datadir` | `CMAKE_INSTALL_DATAROOTDIR` |
| `mandir` | `/share/man` | `--mandir` | `--mandir` | `CMAKE_INSTALL_MANDIR` |
| `infodir` | `/share/info` | `--infodir` | `--infodir` | `CMAKE_INSTALL_INFODIR` |
| `localedir` | `/share/locale` | `--localedir` | `--localedir` | `CMAKE_INSTALL_LOCALEDIR` |
| `docdir` | `/share/doc` | `--docdir` | — | `CMAKE_INSTALL_DOCDIR` |
| `sysconfdir` | `/etc` | `--sysconfdir` | `--sysconfdir` | `CMAKE_INSTALL_SYSCONFDIR` |
| `localstatedir` | `/var` | `--localstatedir` | `--localstatedir` | `CMAKE_INSTALL_LOCALSTATEDIR` |
| `sharedstatedir` | `/var/lib` | `--sharedstatedir` | `--sharedstatedir` | `CMAKE_INSTALL_SHAREDSTATEDIR` |
| `runstatedir` | `/run` | `--runstatedir` | — | `CMAKE_INSTALL_RUNSTATEDIR` |

`pkg-config` cerca in `/lib/pkgconfig` e `/share/pkgconfig`.

Punti da verificare in fase 1 (prefisso `/`):

- **autotools:** con `--prefix=/` le variabili derivate diventano `//bin`,
  `//lib`. Si evita passando sempre tutte le cartelle in modo esplicito, come
  cbuild fa già per quasi tutte.
- **CMake:** con il prefisso `/`, `GNUInstallDirs` antepone `usr/` a tutte le
  cartelle relative. Confermato nella prova di fattibilità: vanno passate come
  percorsi assoluti (`-DCMAKE_INSTALL_LIBDIR=/lib` ecc.).
- **File generati:** i `.pc` e i file di configurazione CMake contengono
  `prefix=/` e quindi percorsi come `//include`. Da normalizzare in un hook.
- **`libexecdir=/lib`:** i pacchetti che installano direttamente in
  `$libexecdir` invece che in `$libexecdir/<pacchetto>` finiscono in `/lib`.
  È il comportamento attuale di Chimera (`/usr/lib`); `path-audit` dovrà
  segnalare gli eseguibili sciolti in `/lib`.

## Percorsi che il kernel si aspetta

| Percorso | Stato |
|----------|-------|
| init | Il kernel prova in ordine `/sbin/init`, `/etc/init`, `/bin/init`, `/bin/sh`: `/bin/init` funziona senza parametri. |
| `/lib/modules` | Già conforme. |
| `/lib/firmware` | Già conforme. |
| `/sbin/modprobe`, `/sbin/hotplug` | Percorsi predefiniti di `kernel.modprobe` e dell'helper uevent: da impostare a `/bin/modprobe` con `CONFIG_MODPROBE_PATH` (o sysctl) e da disattivare l'helper uevent. |
| `/sbin/poweroff`, `/sbin/reboot` | Predefiniti di `kernel.poweroff_cmd`: da impostare via sysctl. |

## Punti aperti

Casi che la §2 del piano non copre. Non sono ancora in `hier.toml`.
Le decisioni proposte, con motivazione, sono in [`decisioni.md`](decisioni.md).

| # | Domanda | Proposta |
|---|---------|----------|
| H-1 | `/var/tmp` (temporanei che sopravvivono al riavvio) | **Chiuso:** vietata; `/tmp` resta l'unica cartella temporanea, in RAM. |
| H-2 | Servizi dinit forniti dai pacchetti | **Chiuso (D-18):** tutto in `/etc/dinit.d`. |
| H-3 | Default di `sysctl`, `modprobe`, `tmpfiles`, `sysusers` che Chimera mette in `/usr/lib/*.d` | **Chiuso (D-18):** tutto in `/etc/<cartella>`. |
| H-4 | Sysroot dei cross-compilatori (`/usr/<tripletta>` in cports) | Non impacchettare i cross-compilatori (solo x86_64). |
| H-5 | Home degli utenti di servizio | `/var/lib/<servizio>`. |
| H-6 | Licenze dei pacchetti | `/share/licenses/<pacchetto>`, come in Chimera senza `/usr`. |
| H-7 | Installazioni affiancate di più versioni (es. LLVM in `/usr/lib/llvm23`) | Obiettivo: una sola versione di LLVM, direttamente in `/bin` e `/lib`. Decisione in fase 1; ripiego: `/lib/llvm<N>/`. |
