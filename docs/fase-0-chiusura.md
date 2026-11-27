# Fase 0 — Chiusura

26 novembre 2026.

**Esito: go su Chimera** (decisione D-10, rischio R-2 del piano).

## Criteri di accettazione

| Criterio | Stato | Dove |
|----------|-------|------|
| D-10, D-11, D-12 registrate con motivazione | Soddisfatto | [`decisioni.md`](decisioni.md) |
| Noto il punto esatto (file e righe) in cui cports definisce il prefisso | Soddisfatto | [`nota-cports.md`](nota-cports.md) §2, [`nota-cports-cbuild.md`](nota-cports-cbuild.md) |

## Deliverable

| Deliverable | Stato |
|-------------|-------|
| `docs/hier.md`, `hier.toml`, `man/hier.7` | Fatto |
| Registro delle decisioni | Fatto: 13 voci prese, una rinviata (H-7) |
| Repository con `CLAUDE.md`, struttura, CI minima | Fatto |
| Nota tecnica su cports | Fatto |
| Prova di fattibilità (non prevista dal piano) | Fatta, esito positivo: [`prova-fattibilita.md`](prova-fattibilita.md) |
| Ambiente di sviluppo sulla macchina personale | **Da fare**: eseguire `image/check-host.sh` |

## Perché go

- Il prefisso `/usr` in cbuild è concentrato in 268 righe; dopo la prima
  modifica ne restano 258 e tre pacchetti si compilano con il layout nuovo.
- I template non vanno riscritti: cbuild traduce i percorsi relativi al
  destdir.
- apk e il driver di clang richiedono molto meno del previsto.
- Il conflitto con `dinit-chimera` è risolto fuori da Chimera, con un pacchetto
  di servizi nostro (D-18b).

## Cosa resta aperto

- **H-7**: LLVM in versione unica, da decidere in fase 1.
- **Verifiche rinviate**: apk-tools e driver di clang sulle versioni esatte
  impacchettate; eliminazione dello script `init`; elenco degli script di
  avvio che restano come eccezioni.
- **Transizione a stadi dell'ambiente di build** (nota tecnica, §7): è il
  rischio principale della fase 1 e non è stato provato.
- **Limiti dell'ambiente cloud**: niente KVM e download dei sorgenti da GitHub
  bloccato. Le build complete e ogni prova di avvio vanno fatte sulla macchina
  personale.

## Cosa cambia nelle fasi successive

Rispetto al piano originale, per effetto delle decisioni prese:

| Fase | Cambiamento |
|------|-------------|
| 1 — Toolchain | Si aggiunge la transizione a stadi dell'ambiente di build. Si decide H-7. Il lavoro su cbuild è già avviato. |
| 2 — Sistema minimo | Niente initramfs (D-22): configurazione del kernel nostra, con i driver di archiviazione comuni ed ext4 inclusi; supporto initrd lasciato attivo; la scelta sul microcodice è rinviata a D-16. Si scrivono qui i servizi di avvio nostri (D-18b), con LVM e RAID (D-20). |
| 3 — Audit dei percorsi | I percorsi letterali nei template non vanno corretti. L'audit deve distinguere tre casi emersi dalla prova: `/usr` funzionale nei sorgenti, residui dell'ambiente di build nei simboli di debug, citazioni in documentazione e commenti. Va aggiunta la normalizzazione di `//` nei file `.pc` e CMake. |
| 4 — Stack di amministrazione | Più piccola: i servizi di avvio sono già fatti. Restano rete, firewall, log, scheduler, dispositivi, generazione della UKI senza initramfs. |
| 5 — Convenzioni di configurazione | Si aggiungono due regole: cosa fare dei file `.apk-new` e come si disabilita un servizio abilitato da un pacchetto (D-18). L'elenco dei pacchetti è `/etc/apk/world` sotto git (D-12). |
| 7 — Uso reale | Il ripristino resta quello del piano: git su `/etc` e UKI precedente (D-21). |

## Cronoprogramma rivisto

Proposta, in settimane di tempo libero (8–10 ore a settimana). Sono stime
grossolane quanto quelle originali.

| Fase | Piano originale | Rivista | Motivo |
|------|-----------------|---------|--------|
| 1 — Toolchain | 3–6 | 4–7 | Transizione a stadi |
| 2 — Sistema minimo | 3–4 | 4–6 | Servizi di avvio, configurazione del kernel nostra |
| 3 — Audit dei percorsi | 3–5 | 2–4 | Niente correzioni ai template |
| 4 — Stack di amministrazione | 4–6 | 3–4 | Servizi di avvio già fatti |
| 5 — Convenzioni di configurazione | 1–2 | 1–2 | — |
| 7 — Uso reale | 4+ | 4+ | — |

Il totale fino alla fase 5 resta nello stesso intervallo (14–23 settimane): il
lavoro si sposta dalle fasi 3 e 4 alle fasi 1 e 2.

## Prossimi passi

1. Sulla macchina personale: `image/check-host.sh`, poi
   `./cbuild binary-bootstrap` e una build di prova (`prova-fattibilita.md`).
2. Fase 1, primo obiettivo: `base-files` e `musl` con il layout nuovo, e un
   "hello world" compilato e avviato in una radice senza `/usr`.
3. In parallelo: prima bozza dei servizi di avvio in `services/`, provata su
   una Chimera normale.
