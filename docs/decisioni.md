# Registro delle decisioni

Ogni decisione ha uno stato:

- **Proposta** — raccomandazione scritta, in attesa di conferma di Vittorio.
- **Presa** — confermata; si cambia solo con una nuova voce che la sostituisce.

Le decisioni D-1…D-7 sono già prese nel piano di progetto (§3.1) e non sono
ripetute qui. Tutte le voci sotto sono **proposte**: nessuna è ancora confermata.

Dati di riferimento: [`nota-cports.md`](nota-cports.md) e
[`prova-fattibilita.md`](prova-fattibilita.md).

---

## D-10 — Base da biforcare: Chimera

**Stato:** proposta. **Data:** 26 novembre 2026.

**Opzioni:** Chimera, Oasis, da zero (stile LFS).

**Decisione:** Chimera, tramite un fork di cports (`vic0824/cports`, branch `nonux`).

**Motivazione**
- Copre già D-2 (dinit), A-8 (userland BSD), musl e clang.
- Il prefisso `/usr` è scritto in chiaro ma concentrato: 268 righe in 38 file
  di cbuild.
- La prova di fattibilità è riuscita su autotools, Meson e CMake con 177 righe
  di modifica, senza toccare i template.
- I percorsi letterali nei template (3390 righe) vengono tradotti da cbuild:
  il costo ricorrente a ogni sincronizzazione (R-8) è molto più basso del
  previsto.
- Oasis ha un layout più vicino al nostro ma un parco software piccolo e un
  sistema di build che andrebbe imparato da zero; da zero significa riscrivere
  le ricette di migliaia di pacchetti.

**Conseguenze**
- Si eredita `dinit-chimera`, che è in conflitto con A-1 e C-3 (vedi D-18).
- Va mantenuto un fork e sincronizzato periodicamente con upstream.

**Quando rivederla:** se in fase 1 `llvm` o `musl` richiedono patch che non
reggono a un aggiornamento di versione, oppure se la transizione a stadi
dell'ambiente di build (nota tecnica, §7) non si chiude.

---

## D-11 — libc: musl

**Stato:** proposta. **Data:** 26 novembre 2026.

**Opzioni:** musl, glibc.

**Decisione:** musl.

**Motivazione**
- È la libc di Chimera: cambiarla significherebbe rinunciare alla base.
- Il loader è già in `/lib/ld-musl-x86_64.so.1`, e il driver di clang lo cerca
  lì: nessuna patch.
- Si configura con `--prefix=/ --syslibdir=/lib`; il template di Chimera oggi
  usa un symlink temporaneo nel destdir che con il nostro layout non serve più.
- glibc ha `/usr` e `/lib64` in molti più punti (ldconfig, locale, gconv, nss).

**Conseguenze:** resta il non-obiettivo già dichiarato sui binari precompilati
per glibc.

**Quando rivederla:** non prevista.

---

## D-12 — Gestore pacchetti: apk

**Stato:** proposta. **Data:** 26 novembre 2026.

**Opzioni:** apk (apk-tools 3), soluzione dichiarativa in stile Oasis.

**Decisione:** apk.

**Motivazione**
- Nel codice non ha `/usr`: usa `lib/apk`, `etc/apk`, `var/cache/apk`.
- È integrato in cbuild; cambiarlo insieme al layout moltiplica i rischi.
- Tratta i file sotto `/etc` come configurazione e non sovrascrive quelli
  modificati: serve per D-18.

**Conseguenze**
- `lib/apk/db` è stato del sistema dentro `/lib`: lo si lascia dov'è, come
  eccezione documentata in `hier.md`, invece di mantenere una patch invasiva.
- `var/log/apk.log` è un file sciolto contro A-6: piccola patch per spostarlo
  in `var/log/apk/`, da fare in fase 4.
- Non si installa nulla in `lib/apk/keys` e `lib/apk/repositories.d`: chiavi e
  repository stanno solo in `/etc/apk` (C-3).

**Da ricontrollare:** l'analisi è sulla versione 3.0.8; cports impacchetta la
3.0.11.

---

## D-18 — Servizi e default dei pacchetti: tutto in `/etc`

**Stato:** proposta. **Data:** 26 novembre 2026. Chiude i punti H-2 e H-3.

**Problema.** Chimera installa i file forniti dai pacchetti in `/usr/lib/*.d`
(`dinit.d`, `tmpfiles.d`, `sysusers.d`, `sysctl.d`, `modprobe.d`,
`modules-load.d`, `binfmt.d`) e riserva `/etc/*.d` alle modifiche
dell'amministratore. È la cascata "default in `lib`, override in `etc`" che
C-3 vuole evitare. Riguarda 98 template con servizi e 81 con `tmpfiles` o
`sysusers`.

**Opzioni**
1. `/lib/*.d` per i pacchetti, `/etc/*.d` per l'amministratore (come Chimera,
   senza `/usr`).
2. Tutto in `/etc/*.d`, una sola cartella per tipo.

**Decisione:** opzione 2.

**Motivazione**
- È l'unica coerente con C-1 e C-3, e con il criterio di accettazione della
  fase 4 (`ls /etc/dinit.d/` mostra tutti i servizi).
- Un solo posto da guardare per sapere cosa parte all'avvio.
- Il rischio dell'opzione 2, cioè perdere le proprie modifiche a un
  aggiornamento, è coperto due volte: apk non sovrascrive i file di `/etc`
  modificati, e `/etc` è sotto git (C-4).

**Conseguenze**
- In cbuild cambiano le destinazioni di `install_service`, `install_tmpfiles`
  e `install_sysusers`, e il lint che oggi vieta `etc/dinit.d` va ribaltato.
- dinit, `sd-tools` e gli helper di `dinit-chimera` vanno configurati per
  leggere una sola cartella.
- Se un pacchetto aggiorna un servizio che l'amministratore ha modificato, apk
  lascia un file `.apk-new` da confrontare a mano: serve una regola nella
  guida di stile (fase 5).

### D-18b — `dinit-chimera`: spostare ora, riscrivere in fase 4

**Stato:** proposta.

`dinit-chimera` contiene 37 script shell di avvio, contro A-1.

**Opzioni:** (1) spostare solo i percorsi; (2) tenere gli helper e riscrivere i
servizi come file dichiarativi; (3) riscrivere l'avvio da zero.

**Decisione:** strada 1 per le fasi 1–3, strada 2 in fase 4.

**Motivazione**
- Fino alla fase 3 l'obiettivo è un sistema che si avvia e passa l'audit dei
  percorsi: riscrivere l'avvio nello stesso momento in cui si cambia la
  toolchain somma due rischi alti.
- La strada 2 conserva gli helper compilati, che sono la parte difficile
  (montaggi, fsck, cryptsetup, zram), e sostituisce solo gli script.
- La strada 3 resta possibile dopo, con un sistema funzionante come confronto.

**Conseguenze:** A-1 non è rispettato fino alla fine della fase 4. La stima
della fase 4 va alzata: non è una conversione meccanica.

---

## Punti minori del layout

Proposte per i punti aperti di `hier.md` non coperti sopra.

| Punto | Decisione proposta | Motivazione |
|-------|--------------------|-------------|
| H-1 `/var/tmp` | Ammessa | `/tmp` è tmpfs: i temporanei grandi o che devono sopravvivere al riavvio non hanno altro posto. |
| H-4 sysroot cross | `/lib/cross/<tripletta>` | Rientra nella regola `/lib/<pacchetto>/`; esiste solo sulle macchine di build. Non urgente: x86_64 è l'unica architettura. |
| H-5 home dei servizi | `/var/lib/<servizio>` | È già "stato dei servizi" secondo `hier.md`. |
| H-6 licenze | `/share/licenses/<pacchetto>` | Come Chimera, senza `/usr`. |
| H-7 versioni affiancate (LLVM) | `/lib/llvm<N>/` con `bin/`, `lib/`, `include/` interni | Rientra in `/lib/<pacchetto>/`. Eccezione a L-1 da documentare: dentro ci sono altri `bin` e `lib`. |
