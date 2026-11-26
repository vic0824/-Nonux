# Nota tecnica — `/usr` in cports

Fase 0, step 3. Stato: prima versione, 26 novembre 2026.

Base analizzata: `chimera-linux/cports`, commit
`f4aac13d0426e3118e12bf4c4ff9f820eb8280aa` (26/11/2026).
I numeri vengono da `tools/usr-inventory/usr_inventory.py` e si rigenerano con:

```
tools/usr-inventory/usr_inventory.py <cports> \
    --csv inventario.csv --md riepilogo.md \
    --core-md docs/nota-cports-cbuild.md \
    --packages tools/usr-inventory/minimal.txt
```

## 1. In sintesi

- Il prefisso `/usr` **non è un parametro** di cports: è scritto in chiaro in
  ogni build style e negli helper dei template. Non c'è un punto unico da
  cambiare, ma i punti sono pochi e tutti in cbuild: 268 righe in 38 file.
- 1143 pacchetti su 3323 citano `usr`. Di questi, 859 (75%) lo fanno con
  percorsi letterali relativi al destdir (`"usr/bin/foo"`), che si riscrivono
  in modo meccanico, e 525 hanno solo quel tipo di riferimento.
- Il sistema minimo (27 pacchetti) ha 394 righe da toccare, 312 delle quali
  meccaniche.
- apk-tools non ha `/usr` nel codice: usa già `lib/apk`, `etc/apk`, `var/cache/apk`.
- Il driver di clang richiede meno del previsto: un'opzione di configurazione
  e una patch di una riga (§5). Il rischio R-1 scende.
- Il problema più grosso non è il prefisso ma `dinit-chimera`: script shell di
  avvio e default in `/usr/lib/*.d`, in conflitto con A-1 e C-3 (§6).

**Indicazione per D-10:** i dati sono a favore di Chimera, e la prova di build
([`prova-fattibilita.md`](prova-fattibilita.md)) è riuscita su tre pacchetti.

## 2. Dove è definito il prefisso

Elenco completo, riga per riga: [`nota-cports-cbuild.md`](nota-cports-cbuild.md).
I punti che contano:

| Cosa | File e righe | Contenuto |
|------|--------------|-----------|
| autotools | `src/cbuild/util/gnu_configure.py:84-91` | `--prefix=/usr`, `--sbindir=/usr/bin`, `--bindir`, `--libdir`, `--libexecdir=/usr/lib`, `--mandir`, `--infodir` |
| libtool | `src/cbuild/util/gnu_configure.py:8` | `lt_cv_sys_lib_dlsearch_path_spec` con `/usr/lib64 /usr/lib32 /usr/lib /lib /usr/local/lib` |
| Meson | `src/cbuild/util/meson.py:84-92` | `--prefix=/usr` e sette cartelle derivate |
| Meson, cross file | `src/cbuild/util/meson.py:36` | `llvm-config = '/usr/bin/llvm-config'` |
| CMake | `src/cbuild/util/cmake.py:103` | `-DCMAKE_INSTALL_PREFIX=/usr` |
| CMake, strumenti | `src/cbuild/util/cmake.py:83-85` | `CMAKE_AR`, `CMAKE_NM`, `CMAKE_RANLIB` in `/usr/bin` |
| Makefile | `src/cbuild/build_style/makefile.py:11,40` | `PREFIX=/usr` |
| waf | `src/cbuild/build_style/waf.py:12-13` | `--prefix=/usr`, `--libdir=/usr/lib` |
| Cargo | `src/cbuild/util/cargo.py:39,247,306` | radice di installazione `/usr` |
| Helper dei template | `src/cbuild/core/template.py:2175-2485` | `install_bin`, `install_lib`, `install_man`, `install_license`, `install_completion`, `install_service`, `install_tmpfiles`, `install_sysusers`, `install_shell`, `uninstall` |
| Sysroot cross | `src/cbuild/core/profile.py:409` | `/usr/<tripletta>` |
| Percorsi di LLVM | `src/cbuild/core/profile.py:172,217,241` | `/usr/lib/llvm<N>/...` |
| `PATH` nel bldroot | `src/cbuild/core/chroot.py:680` | `/usr/bin` |
| wrapper pkg-config | `src/cbuild/hooks/prepare/000_script_wrapper.py:25-40` | `{sysroot}/usr/lib/pkgconfig`, `/usr/bin/pkg-config` |
| Lint | `src/cbuild/hooks/pkg/098_lint.py:181-289` | vieta percorsi *sotto* `/usr` e sposta roba da `/etc` a `/usr`: logica da ribaltare |
| Dipendenze runtime | `src/cbuild/hooks/pkg/001_runtime_deps.py:75` | cerca le librerie in `/usr/lib` |
| Shebang Python | `src/cbuild/hooks/destdir/100_rewrite_python_shebang.py:7,35` | riscrive verso `/usr/bin/python3` |
| Symlink FHS | `main/base-files/template.py:62-75` | `/bin → usr/bin`, `/lib → usr/lib`, `/sbin`, `/usr/sbin`, `lib64` |

## 3. Numeri

### Riepilogo per categoria

| Cat. | Descrizione | Righe | File | Pacchetti |
|---|---|---:|---:|---:|
| A | cbuild: build style, util, hook, profili | 176 | 37 | — |
| B | cbuild: helper dei template (core/template.py) | 92 | 1 | — |
| C | template: percorso letterale relativo al destdir | 3390 | 859 | 859 |
| D1 | template: argomento di configurazione | 613 | 314 | 314 |
| D2 | template: percorso assoluto in altra logica | 266 | 145 | 145 |
| E | patch: righe aggiunte con /usr | 351 | 112 | 98 |
| G | file ausiliari del pacchetto | 663 | 429 | 242 |

### Pacchetti toccati

| Repo | Template | Con almeno un riferimento | Solo categoria C |
|---|---:|---:|---:|
| main | 2384 | 861 | 411 |
| user | 939 | 282 | 114 |

### Pacchetti del sistema minimo

| Pacchetto | C | D1 | D2 | E | G | Totale |
|---|---:|---:|---:|---:|---:|---:|
| main/base-files | 19 | 0 | 0 | 0 | 22 | 41 |
| main/musl | 18 | 1 | 0 | 1 | 0 | 20 |
| main/linux-headers | 3 | 0 | 0 | 0 | 0 | 3 |
| main/llvm23 | 25 | 5 | 4 | 3 | 2 | 39 |
| main/chimerautils | 12 | 1 | 1 | 0 | 3 | 17 |
| main/dinit | 0 | 1 | 0 | 0 | 0 | 1 |
| main/dinit-chimera | 8 | 1 | 4 | 0 | 5 | 18 |
| main/apk-tools | 7 | 0 | 0 | 0 | 0 | 7 |
| main/util-linux | 143 | 1 | 0 | 0 | 2 | 146 |
| main/linux-stable | 2 | 0 | 0 | 0 | 0 | 2 |
| main/zlib-ng-compat | 0 | 1 | 0 | 0 | 0 | 1 |
| main/openssl3 | 2 | 1 | 0 | 0 | 0 | 3 |
| main/zstd | 2 | 5 | 0 | 0 | 0 | 7 |
| main/xz | 3 | 0 | 0 | 0 | 0 | 3 |
| main/bzip2 | 11 | 0 | 0 | 0 | 2 | 13 |
| main/libarchive | 9 | 0 | 0 | 0 | 0 | 9 |
| main/ncurses | 21 | 2 | 1 | 0 | 0 | 24 |
| main/libedit | 11 | 0 | 0 | 0 | 0 | 11 |
| main/libxo | 1 | 0 | 0 | 0 | 0 | 1 |
| main/libcap | 0 | 4 | 0 | 0 | 0 | 4 |
| main/acl | 1 | 0 | 0 | 0 | 0 | 1 |
| main/attr | 2 | 0 | 0 | 0 | 0 | 2 |
| main/pkgconf | 6 | 0 | 0 | 0 | 0 | 6 |
| main/gmake | 1 | 0 | 0 | 0 | 0 | 1 |
| main/fakeroot | 1 | 0 | 0 | 0 | 0 | 1 |
| main/kmod | 1 | 0 | 0 | 0 | 7 | 8 |
| main/turnstile | 3 | 1 | 1 | 0 | 0 | 5 |
| **Totale** | 312 | 24 | 11 | 4 | 43 | 394 |

### I 20 pacchetti con più riferimenti

| Pacchetto | Righe |
|---|---:|
| main/util-linux | 146 |
| main/samba | 116 |
| main/cryptsetup-scripts | 91 |
| user/gcc | 61 |
| main/initramfs-tools | 57 |
| main/qt6-qtbase | 53 |
| main/lvm2 | 51 |
| main/nfs-utils | 50 |
| user/postgresql16 | 50 |
| main/base-kernel | 48 |
| main/heimdal | 48 |
| main/qemu | 45 |
| main/base-files | 41 |
| main/php8.3 | 40 |
| main/qt6-qtdeclarative | 40 |
| main/llvm23 | 39 |
| main/udev | 34 |
| main/binutils | 32 |
| main/git | 32 |
| main/systemd-boot | 32 |

Come leggere le categorie:

- **A, B** si correggono una volta sola, in cbuild.
- **C** non richiede modifiche ai template: nella prova di fattibilità cbuild
  traduce da solo i percorsi `"usr/..."` relativi al destdir. Niente codemod e
  niente costo ricorrente a ogni sincronizzazione (R-8).
- **D1** è quasi sempre meccanica (`--libdir=/usr/lib`), ma va letta: alcuni
  argomenti indicano dove *cercare* una dipendenza, non dove installare.
- **D2, E, G** vanno guardate una per una.

Limite dell'inventario: conta ciò che è scritto in cports, non ciò che è
scritto nei sorgenti dei programmi. Quel costo si misura solo compilando
(step 5) e con `path-audit` (fase 3).

## 4. apk-tools

Percorsi fissi nel codice (letti dal mirror GitHub, versione 3.0.8; cports
impacchetta la 3.0.11, da ricontrollare sul tarball esatto):

| Percorso | Uso |
|----------|-----|
| `lib/apk/db/` | Database dei pacchetti installati, lock |
| `lib/apk/exec/` | Script dei pacchetti |
| `etc/apk/` | `world`, `repositories`, `keys`, `arch`, `config`, `protected_paths.d` |
| `lib/apk/{keys,repositories.d,commit_hooks.d,config}` | Default forniti dalla distro, con override in `etc/apk/` |
| `var/cache/apk` | Cache |
| `var/log/apk.log` | Log |
| `/usr/sbin/uvol` | Solo con i volumi uvol (OpenWrt): non ci riguarda |

Tutti compatibili con il layout. Due osservazioni:

- `var/log/apk.log` è un file sciolto, contro A-6 (`/var/log/<servizio>/`):
  piccola patch o eccezione documentata.
- apk ha anch'esso la coppia "default in `lib/apk`, override in `etc/apk`":
  per C-3 basta non installare nulla in `lib/apk/{keys,repositories.d}`.
  `lib/apk/db` è stato, non configurazione: andrebbe in `/var/lib/apk`, ma
  spostarlo richiede una patch invasiva. Proposta: lasciarlo dov'è.

Il template di Chimera installa `usr/lib/apk/config` e `base-files` crea
`usr/lib/apk/exec`: diventano `lib/apk/...`, che è dove apk li cerca già.

**Indicazione per D-12:** apk, nessun ostacolo.

## 5. Toolchain: clang e musl

Driver di clang (`clang/lib/Driver/ToolChains/Linux.cpp`, ramo `main` di LLVM;
da ricontrollare sulla 23.1.6 impacchettata da cports):

| Punto | Comportamento | Cosa serve |
|-------|---------------|------------|
| Header C | Aggiunge `/include` e poi `/usr/include`. Se però LLVM è configurato con `-DC_INCLUDE_DIRS=...`, usa solo quell'elenco e salta entrambi. | `-DC_INCLUDE_DIRS=/include` nel template: nessuna patch |
| `/usr/local/include` | Aggiunto sempre, prima del resto | Patch di una riga |
| Librerie | `/lib` e `/usr/lib` aggiunti solo se esistono (`addPathIfExists`) | Niente: senza `/usr` spariscono da soli |
| Loader musl | `/lib/ld-musl-<arch>.so.1` | Già conforme |
| Header di libc++ | Cercati relativamente alla cartella del compilatore | Dipende da dove si installa LLVM (sotto) |
| Multiarch | Già disattivato su musl dalla patch 0013 di Chimera | Niente |

Chimera installa LLVM in un prefisso proprio, `/usr/lib/llvm23`, e mette in
`/usr/bin` e `/usr/lib` dei symlink. Il template (`main/llvm23/template.py`)
ha 39 righe con `usr` e contiene la logica di bootstrap
(`/usr/lib/llvm-bootstrap`): è il template più delicato del sistema minimo.
Con il nostro layout diventa `/lib/llvm23/` (punto H-7 di `hier.md`).

musl: `--prefix=/usr` in `main/musl/template.py:7`, più un symlink
`lib → usr/lib` creato dentro il destdir (riga 139) per far finire il loader
in `/usr/lib`. Con `--prefix=/ --syslibdir=/lib` quel trucco non serve più.

lld non ha percorsi di ricerca predefiniti: li riceve dal driver.

## 6. dinit-chimera: il conflitto vero

`dinit-chimera` è il pacchetto che porta il sistema dall'avvio del kernel al
login. Nel suo repository (HEAD) ci sono 55 servizi e **37 script shell** in
`early/scripts/`, più helper compilati. Inoltre si appoggia a una serie di
cartelle di default in `/usr/lib`:

| Cartella | Usata da | Pacchetti coinvolti |
|----------|----------|---------------------|
| `/usr/lib/dinit.d` | servizi dei pacchetti | 98 template chiamano `install_service` |
| `/usr/lib/tmpfiles.d`, `/usr/lib/sysusers.d` | creazione di file e utenti all'avvio | 81 template |
| `/usr/lib/sysctl.d`, `modprobe.d`, `modules-load.d`, `binfmt.d` | impostazioni del kernel | dinit-chimera e pochi altri |

Tutte seguono lo schema "default del pacchetto in `lib`, override
dell'amministratore in `etc`", cioè la cascata che C-3 vuole evitare, e gli
script di avvio sono contro A-1.

Non è un problema di fase 0, ma condiziona la stima della fase 4, che nel piano
parla di "convertire i servizi" come lavoro meccanico. Le strade:

1. **Tenere dinit-chimera** spostando solo i percorsi (`/lib/dinit.d` ecc.).
   Costo basso, ma A-1 e C-3 restano violati nel cuore del sistema.
2. **Tenere gli helper, riscrivere i servizi di avvio** come file dichiarativi
   che chiamano direttamente i comandi. Costo medio; gli script più lunghi
   (fsck, root rw, cryptsetup, zram) non si riducono a una riga.
3. **Riscrivere l'avvio** con un set minimo di servizi propri. Costo alto, ma
   è l'unica strada pienamente coerente con gli obiettivi.

Decisioni prese dopo aver letto il codice: D-18 e D-18b in
[`decisioni.md`](decisioni.md). La descrizione qui sopra è superata in due
punti: gli script sono 36 (circa 790 righe, in gran parte involucri), e la
strada scelta è un pacchetto di servizi nostro, scritto in fase 2.

## 7. Il bldroot: un problema di ordine

cbuild compila dentro un ambiente fatto con gli stessi pacchetti che produce.
Finché l'ambiente è una Chimera normale, i percorsi assoluti di cbuild
(`/usr/bin/pkg-config`, `/usr/lib/llvm23`, il `PATH`) sono corretti; appena i
pacchetti di base cambiano layout, anche l'ambiente lo cambia. La transizione
va quindi fatta in tre passaggi, come il bootstrap a stadi che cbuild ha già:

1. ambiente Chimera standard → pacchetti con il layout nuovo;
2. ambiente fatto con quei pacchetti → ricompilazione di tutto;
3. verifica che il risultato del passo 2 sia identico rifacendolo.

Per questo cbuild deve poter distinguere il layout dell'ambiente in cui gira da
quello dei pacchetti che produce, almeno durante il passo 1.

## 8. Stima dello sforzo

Stime grossolane, in ore di lavoro, da correggere dopo lo step 5.

| Lavoro | Dimensione | Stima | Rischio |
|--------|-----------|-------|---------|
| Rendere parametrico cbuild (A + B) | 268 righe, 38 file | 10–15 h, di cui una prima parte già fatta | Medio: va mantenuto a ogni sync |
| Doppio layout per la transizione (§7) | profilo + bootstrap | 10–20 h | Alto |
| Categoria C | 3390 righe, 859 pacchetti | 0 h: tradotta da cbuild (vedi prova di fattibilità) | Basso |
| Template del sistema minimo (D1, D2, E, G) | 82 righe, 27 pacchetti | 8–12 h | Medio |
| `llvm23` e `musl` | 59 righe, logica di bootstrap | 15–30 h | Alto (R-1) |
| `base-files` | 41 righe | 3–5 h | Basso |
| Servizi di avvio nostri (D-18b) | una ventina di servizi, poche eccezioni in shell | da stimare all'inizio della fase 2; molto meno delle 60+ h ipotizzate all'inizio | Medio |
| `/usr` nei sorgenti dei programmi | ignoto | da misurare allo step 5 | — |

Fuori dal sistema minimo, i pacchetti più costosi in cports sono `samba` (116
righe), `cryptsetup-scripts` (91), `gcc` (61), `initramfs-tools` (57),
`qt6-qtbase` (53), `lvm2` (51).

## 9. Cosa manca

- Ricontrollare apk-tools e il driver di clang sulle versioni esatte
  impacchettate (3.0.11 e 23.1.6).
- Estendere la prova di build a `base-files`, `musl` e a un pacchetto con
  servizi dinit, e provare a installare i pacchetti prodotti in una radice vuota.
