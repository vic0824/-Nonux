# Prova di fattibilità — prefisso `/` in cbuild

Fase 0, step 5. 26 novembre 2026.

**Esito: positivo.** Con una modifica contenuta a cbuild, tre pacchetti (uno
autotools, uno Meson, uno CMake) si compilano e producono pacchetti `.apk` senza
nessun file sotto `usr/`. Senza la nuova opzione cbuild si comporta come prima.

## Cosa è stato fatto

Modifica sul branch `nonux` del fork di cports, commit `e24d6d6`:
11 file, 108 righe aggiunte e 41 tolte, più un modulo nuovo di 80 righe.

- **`src/cbuild/core/layout.py`** (nuovo): unico punto in cui è definito il
  prefisso. Si sceglie con la variabile d'ambiente `CBUILD_TARGET_PREFIX`
  (`/usr`, predefinito, oppure `/`).
- **Sistemi di build** (`gnu_configure.py`, `meson.py`, `cmake.py`,
  `makefile.py`): le cartelle di installazione vengono dal modulo.
- **Traduzione dei percorsi nel destdir.** Template e hook scrivono
  `self.destdir / "usr/bin/foo"`. Invece di riscriverli tutti, il destdir è
  diventato un oggetto che, con il prefisso `/`, toglie da solo il componente
  `usr/`. La traduzione avviene dentro cbuild, non sul filesystem: non è un
  symlink di compatibilità e non viola L-3.
- **Hook adattati**: controllo dei percorsi dei file ELF, lint delle cartelle di
  primo livello, file di debug (`/lib/debug`), controllo delle licenze.

## Risultati

Ambiente: bldroot Chimera standard (`cbuild binary-bootstrap`), x86_64.

| Pacchetto | Sistema di build | Esito | Sottopacchetti |
|-----------|------------------|-------|----------------|
| `pkgconf` 2.4.3 | autotools | passa | 8 |
| `serd` 0.32.10 | Meson | passa | 7 |
| `cmocka` 1.1.8 | CMake | passa | 3 (uno è `-dbg`, non contato sotto) |

Verifiche:

- 19 pacchetti `.apk`, 47 file: **nessuno sotto `usr/`**. Cartelle di primo
  livello: `bin` (4), `include` (8), `lib` (24), `share` (11).
- Tolto il prefisso, l'elenco dei file è identico a quello della build normale.
  Unica differenza voluta: i simboli di debug passano da
  `usr/lib/debug/usr/bin/x` a `lib/debug/bin/x`.
- Senza `CBUILD_TARGET_PREFIX` gli elenchi dei file sono identici a quelli
  prodotti da cbuild non modificato.
- I template dei tre pacchetti **non sono stati toccati**: la suddivisione in
  sottopacchetti (`-devel`, `-libs`, `-progs`, `-man`, `-doc`) funziona grazie
  alla traduzione dei percorsi.

## Cosa ha insegnato

1. **La categoria C dell'inventario quasi sparisce.** Le 3390 righe con
   percorsi letterali `"usr/..."` nei template passano per il destdir e vengono
   tradotte da cbuild. Non serve un codemod né va rifatto a ogni
   sincronizzazione: il costo ricorrente previsto da R-8 scende molto. Restano
   fuori le righe che costruiscono il percorso come stringa
   (`f"{self.chroot_destdir}/usr/share/man"`), che sono nelle categorie D1 e D2.
2. **Il caso speciale di CMake è confermato.** Con prefisso `/`,
   `GNUInstallDirs` antepone `usr/` a tutte le cartelle relative, anche a quelle
   passate dall'utente: al primo tentativo `cmocka` ha installato in `usr/lib`.
   Si risolve passando percorsi assoluti (`-DCMAKE_INSTALL_LIBDIR=/lib` ecc.).
3. **La doppia barra esiste, ma solo nei file generati.** I file `.pc` e i file
   di configurazione CMake contengono `prefix=/` e quindi
   `includedir=${prefix}/include`, cioè `//include`. Funziona, ma è brutto e
   qualche programma potrebbe confrontare i percorsi come stringhe. Si può
   normalizzare in un hook dopo l'installazione; cbuild ne ha già uno che
   riscrive i `.pc`.
4. **`/usr` nei sorgenti: primo caso reale.** `libpkgconf` contiene la stringa
   `/usr/local/share:/usr/share`, valore predefinito di `XDG_DATA_DIRS` scritto
   nel codice. I percorsi configurabili invece sono giusti
   (`/lib/pkgconfig:/share/pkgconfig`, `/include`, `/lib`). È il tipo di
   problema che `path-audit` dovrà trovare e che richiede una patch al sorgente.
5. **Falsi positivi per `path-audit`.** Le librerie statiche contengono
   `/usr/include/...` nelle informazioni di debug, perché sono state compilate
   in un ambiente che ha ancora `/usr`: sparirà quando anche l'ambiente di build
   avrà il layout nuovo. Documentazione e commenti (`README.md`, un commento in
   `cmocka-config.cmake`) citano `/usr` senza conseguenze. L'audit dovrà
   distinguere i tre casi.

## Limiti

- Tre pacchetti piccoli e senza dipendenze particolari: dimostrano che il
  meccanismo regge, non che reggerà su `llvm`, `musl` o `util-linux`.
- Cambia solo il layout dei pacchetti prodotti. L'ambiente di build resta una
  Chimera normale, quindi i pacchetti non sono ancora installabili insieme:
  manca `base-files` e manca la transizione a stadi descritta nella nota
  tecnica (§7).
- Non sono stati adattati: sysroot per la cross-compilazione, Cargo, waf,
  wrapper di `pkg-config`, hook delle dipendenze runtime per le librerie, gli
  helper `install_service`, `install_tmpfiles` e simili (funzionano per
  traduzione, ma la destinazione dipende dalla decisione D-18).
- La scelta del layout con una variabile d'ambiente è provvisoria: va spostata
  nel profilo di build o in `etc/config.ini`.
- I pacchetti prodotti non sono stati installati né eseguiti.

## Come ripetere la prova

```
cd cports
./cbuild keygen && ./cbuild binary-bootstrap          # una volta sola
CBUILD_TARGET_PREFIX=/ ./cbuild -r packages-nonux pkg main/pkgconf
CBUILD_TARGET_PREFIX=/ ./cbuild -r packages-nonux pkg main/serd
CBUILD_TARGET_PREFIX=/ ./cbuild -r packages-nonux pkg main/cmocka
```

cbuild va eseguito da un utente normale, non da root, e richiede `bwrap`, un
`apk` statico di Chimera e `ruff` (o `flake8` e `black`).
