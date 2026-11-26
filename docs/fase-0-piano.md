# Fase 0 — Piano operativo

Riferimento: *Piano di progetto*, §4 Fase 0 e §8 "Prossimi passi".
Stato: bozza, 26 novembre 2026.

Avanzamento:
- Step 1 (specifica del layout): fatto — `hier.md`, `hier.toml`, `man/hier.7`.
  Restano i punti aperti H-1…H-7 elencati in `hier.md`.
- Step 3 (nota tecnica): prima versione in `nota-cports.md`.
- Step 2: in attesa del fork di cports. Step 4–8: da fare.

Obiettivo della fase: avere una specifica del layout scritta, le decisioni
D-10/D-11/D-12 chiuse con motivazione, una mappa precisa dei punti in cui
cports assume `/usr`, e un repository pronto per le fasi successive.
La fase si chiude con la decisione go/no-go sulla base (rischio R-2).

---

## 0. Primo sopralluogo su cports (già fatto)

Clone superficiale di `chimera-linux/cports` (commit `f4aac13`, 26/11/2026).
Dati grezzi, da raffinare nello step 3:

| Punto | Dove | Osservazione |
|-------|------|--------------|
| Prefisso autotools | `src/cbuild/util/gnu_configure.py:84-91` | `--prefix=/usr`, `--bindir`, `--sbindir=/usr/bin`, `--libdir`, `--libexecdir=/usr/lib`, `--mandir`, `--infodir` fissi |
| Prefisso Meson | `src/cbuild/util/meson.py:84-92` | Stessa lista, fissa; anche `llvm-config = '/usr/bin/llvm-config'` (riga 36) |
| Prefisso CMake | `src/cbuild/util/cmake.py:103` | `-DCMAKE_INSTALL_PREFIX=/usr`; righe 83-85 strumenti in `/usr/bin` |
| Makefile / waf | `build_style/makefile.py:11,40`, `build_style/waf.py:12-13` | `PREFIX=/usr` |
| Helper dei template | `src/cbuild/core/template.py:2314-2444` | `install_bin`, `install_lib`, `install_man`, `install_license`, `install_service` (→ `usr/lib/dinit.d`), completions, ecc. scrivono in `usr/...` |
| Sysroot cross | `src/cbuild/core/profile.py:409` | `/usr/<triplet>` |
| Percorsi LLVM | `src/cbuild/core/profile.py:172,217,241` | `/usr/lib/llvm<ver>/...` |
| Lint | `src/cbuild/hooks/pkg/098_lint.py:181-215` | Elenco di percorsi vietati *sotto* `/usr`: va ribaltato (vietare `/usr` stesso) |
| Shebang Python | `hooks/destdir/100_rewrite_python_shebang.py` | Riscrive verso `/usr/bin/python3`: base utile per lo `shebang-fix` della fase 3 |
| Symlink FHS | `main/base-files/template.py:62-75` | Crea `/bin → usr/bin`, `/lib → usr/lib`, `/sbin`, `lib64`: Chimera è *usr-merged al contrario* rispetto a noi |
| musl | `main/musl/template.py:7,137-163` | `--prefix=/usr`, loader in `usr/lib` |

Conteggio: 210 occorrenze di `"usr...` in `src/cbuild`; **820 template su
2384** in `main/` e **251 su 939** in `user/` contengono `usr` esplicitamente;
634 file di patch in `main/` lo citano.

Prime conseguenze:
- Il prefisso **non è parametrico**: va introdotto un unico punto di verità
  (es. `self.prefix` / variabili di profilo) e fatto usare a tutti i
  build style e helper. Questa è la patch "generica" proponibile upstream (R-8).
- Gli 820 template con `usr` esplicito si dividono in due classi da misurare:
  sostituzione meccanica (`"usr/bin"` → helper) e casi con logica propria.
- Conflitto da chiarire con C-1: Chimera installa i servizi in
  `/usr/lib/dinit.d` (default del pacchetto) e lascia `/etc/dinit.d` all'admin.
  Con la regola C-3 ("nessun default nascosto") va deciso se i servizi dei
  pacchetti vanno in `/etc/dinit.d` o in `/lib/dinit.d` → nuova decisione **D-18**.
- Il sysroot cross `/usr/<triplet>` esiste solo sull'host di build, ma per L-2
  va comunque spostato (es. `/lib/cross/<triplet>` o fuori dall'albero).

---

## Step

Ordine pensato per anticipare le informazioni che servono al go/no-go.
Ogni step ha un output e un criterio di "fatto".

### Step 1 — Specifica del layout (`docs/hier.md`, `hier(7)`)

1. Trascrivere la §2 del piano in `docs/hier.md`, aggiungendo per ogni cartella:
   variabili di build corrispondenti (`prefix`, `bindir`, `sbindir`, `libdir`,
   `libexecdir`, `includedir`, `datadir`, `sysconfdir`, `localstatedir`,
   `runstatedir`, `mandir`, `infodir`, `pkgconfigdir`), valori attesi per
   autotools, Meson e CMake.
2. Chiudere i casi non coperti dalla §2: `/var/tmp`, `/var/run`(vietato o no),
   `/lib/firmware`, `/share/licenses`, home di servizio, `/etc/skel`, posto dei
   servizi dinit dei pacchetti (D-18), sysroot cross.
3. Ricavare la pagina man `hier(7)` in mdoc (stile BSD, coerente con A-8).
4. Produrre una versione machine-readable (`docs/hier.toml`: elenco
   consentiti/vietati) che userà `path-audit` in fase 3 e la CI qui.

**Fatto quando:** `docs/hier.md` e `hier.7` esistono, `mandoc -Tlint` passa,
`hier.toml` è validato da un test.

### Step 2 — `CLAUDE.md` e struttura del repository

1. Creare la struttura di §6.2: `docs/`, `tools/path-audit/`,
   `tools/shebang-fix/`, `services/`, `etc-template/`, `image/`, `ci/`.
2. `CLAUDE.md`: layout consentito/vietato (rimando a `hier.md`), regola "mai
   symlink di compatibilità", convenzioni di patch (header con motivazione,
   una patch per problema), comandi per lint e audit.
3. Decidere come includere cports: **submodule** su un fork
   (`<utente>/cports`, branch `nonux`) — consigliato, tiene separata la storia
   upstream e semplifica i rebase (R-8) — oppure subtree.

**Fatto quando:** struttura e `CLAUDE.md` committati; cports agganciato al
commit upstream di riferimento.

### Step 3 — Nota tecnica su cports (inventario `/usr`)

È il criterio di accettazione "punto esatto (file e righe)". Lavoro adatto a
Claude Code.

1. Script `tools/usr-inventory/` (Python) che scansiona cports e produce un
   report CSV/Markdown: file, riga, categoria.
2. Categorie:
   - **A — cbuild core** (build style, util, hooks, profile): da rendere parametrico;
   - **B — helper dei template**: si correggono una volta in `template.py`;
   - **C — template con percorso letterale sostituibile meccanicamente**;
   - **D — template con logica propria** (symlink, move, sed su file);
   - **E — patch upstream** che contengono `/usr`;
   - **F — pacchetti che "forzano" `/usr` nel loro build system**
     (da scoprire con build di prova nello step 5).
3. Stima dello sforzo per categoria (ore, rischio) e per i ~30 pacchetti del
   sistema minimo della fase 2 (musl, llvm, chimerautils, dinit, dinit-chimera,
   apk-tools, base-files, util-linux, dash/sh, kernel, …) elencati per nome.
4. Analisi di apk-tools: percorsi fissi (`/lib/apk/db`, `/etc/apk`,
   `/usr/lib/apk/exec`) — input per D-12.
5. Analisi del driver clang (`clang/lib/Driver/ToolChains/Linux.cpp`, patch di
   Chimera in `main/llvm/patches/`): quanti percorsi `/usr` e se basta
   `DEFAULT_SYSROOT`/config file — anticipa R-1.

**Fatto quando:** `docs/nota-cports.md` contiene la tabella dei punti con
file:riga, la classificazione e la stima.

### Step 4 — Registro delle decisioni D-10, D-11, D-12 (+ D-18)

Formato ADR leggero in `docs/decisioni.md`: contesto, opzioni, decisione,
motivazione, conseguenze, condizioni di revisione.

- **D-10 base**: confronto Chimera / Oasis / da zero alla luce dello step 3.
  Criterio quantitativo proposto: se le categorie A+B+C coprono la grande
  maggioranza delle occorrenze del sistema minimo, Chimera è go.
- **D-11 libc**: musl; verificare solo che `--syslibdir=/lib` sia sufficiente.
- **D-12 pacchetti**: apk, con l'elenco dei percorsi fissi trovati.
- **D-18 servizi dinit dei pacchetti**: `/lib/dinit.d` vs `/etc/dinit.d`.

**Fatto quando:** le quattro decisioni sono registrate con motivazione.

### Step 5 — Esperimento di fattibilità (spike)

Per non decidere il go/no-go solo su grep:

1. Branch del fork cports con il prefisso reso parametrico solo in cbuild
   (categoria A+B), valore `/`.
2. Build di 3 pacchetti campione: uno autotools (es. `gzip`), uno Meson
   (es. `libinih` o `pkgconf`), uno CMake (es. `zstd`), dentro il bldroot
   Chimera standard.
3. Verifica del `destdir`: nessun file sotto `usr/`, nessuna doppia barra.

**Fatto quando:** i tre pacchetti producono un `destdir` conforme, oppure è
documentato perché no.

### Step 6 — Ambiente di sviluppo (macchina personale)

Va fatto sulla macchina personale, **non** in questa sessione cloud (qui non
c'è `/dev/kvm`, ci sono 4 core e circa 60 GB liberi; cbuild e gli spike leggeri
invece girano anche qui).

1. Requisiti: Linux con KVM, QEMU + OVMF, ≥ 100 GB, `bubblewrap` (cbuild lo
   usa per il bldroot), Python ≥ 3.12, git, `mandoc`.
2. Script `image/check-host.sh` che verifica i requisiti e stampa cosa manca.
3. Bootstrap del bldroot cbuild da pacchetti binari Chimera
   (`./cbuild binary-bootstrap`) e build di prova di un pacchetto non modificato.

**Fatto quando:** `check-host.sh` passa e un pacchetto Chimera standard si
compila.

### Step 7 — CI minima

GitHub Actions:
- lint Markdown/`mandoc -Tlint` su `hier.7`;
- test dello schema `hier.toml`;
- esecuzione di `usr-inventory` con pubblicazione del report come artifact
  (così il numero di occorrenze `/usr` diventa una metrica che scende nel tempo);
- (più avanti) build dei pacchetti campione dello step 5.

**Fatto quando:** la CI gira verde sul branch.

### Step 8 — Chiusura della fase

1. Rivedere le stime del cronoprogramma (§7) con i dati dello step 3 e 5.
2. Decisione go/no-go su Chimera, registrata in `docs/decisioni.md`.

---

## Dipendenze tra gli step

```
1 ──► 2 ──► 3 ──► 4 ──► 8
            │     ▲
            └──► 5┘
6 (in parallelo, sulla macchina personale) ──► 5 (build complete)
7 dopo 1-3
```

Gli step 1, 2, 3 e 7 si possono fare interamente in questa sessione; lo step 5
probabilmente anche (va verificato che bubblewrap funzioni nel container); lo
step 6 richiede la macchina personale.
