# Registro delle decisioni

Ogni decisione ha uno stato:

- **Proposta** — raccomandazione scritta, in attesa di conferma di Vittorio.
- **Presa** — confermata; si cambia solo con una nuova voce che la sostituisce.

Le decisioni D-1…D-7 sono già prese nel piano di progetto (§3.1) e non sono
ripetute qui.

| ID | Argomento | Stato |
|----|-----------|-------|
| D-10 | Base: Chimera | presa |
| D-11 | libc: musl | presa |
| D-12 | Pacchetti: apk, con l'elenco dei pacchetti in `/etc/apk/world` | presa |
| D-16 | Avvio: UKI e microcodice | rinviata alla fase 4 |
| D-18 | Servizi e default dei pacchetti in `/etc` | presa |
| D-18b | Avvio: servizi nostri in fase 2, shell solo come eccezione documentata | presa |
| D-19 | Nessuna cifratura del disco | presa |
| D-20 | LVM e RAID software sì; zram e kdump no | presa |
| D-21 | ext4, nessuno snapshot | presa |
| D-22 | Nessun initramfs, radice su partizione semplice | presa |
| H-1 | `/tmp` in RAM, `/var/tmp` vietata | presa |
| H-7 | LLVM in versione unica | obiettivo, decisione rinviata alla fase 1 |
| H-4 | Cross-compilatori non impacchettati | presa |
| H-5 | Home dei servizi in `/var/lib/<servizio>` | presa |
| H-6 | Licenze in `/share/licenses/<pacchetto>` | presa |

Dati di riferimento: [`nota-cports.md`](nota-cports.md) e
[`prova-fattibilita.md`](prova-fattibilita.md).

---

## D-10 — Base da biforcare: Chimera

**Stato:** presa (Vittorio, 26 novembre 2026).

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

**Stato:** presa (Vittorio, 26 novembre 2026).

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

**Stato:** presa (Vittorio, 26 novembre 2026).

**Opzioni:** apk (apk-tools 3), soluzione dichiarativa in stile Oasis.

**Decisione:** apk, usato in modo dichiarativo: l'elenco dei pacchetti
richiesti è il file `/etc/apk/world`, che sta sotto git con il resto di
`/etc`. Installare o rimuovere un pacchetto equivale a modificare quel file e
far riallineare il sistema.

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

## D-16 — Avvio: UKI e microcodice

**Stato:** rinviata alla fase 4, quando si scrive la generazione della UKI.

**Già fissato da D-22:** la UKI contiene il kernel e la riga di comando, con la
radice indicata per `PARTUUID`. Non contiene un initramfs.

**Da decidere: come si carica il microcodice della CPU.**
- (a) Un archivio separato che contiene solo il file del microcodice, senza
  script né programmi, che il kernel riceve come initrd e che la UKI include.
  Un aggiornamento del microcodice non richiede di ricompilare il kernel.
- (b) Il microcodice incluso nel kernel, da ricompilare a ogni aggiornamento.
- (c) Non caricarlo e affidarsi al firmware della scheda madre.

La preferita è (a). Dipende da come si avvia il kernel e si può verificare solo
su hardware reale, perché in macchina virtuale il microcodice non si carica.
Per non chiudere questa strada, il kernel di fase 2 tiene attivo
`CONFIG_BLK_DEV_INITRD` (D-22).

---

## D-18 — Servizi e default dei pacchetti: tutto in `/etc`

**Stato:** presa (confermata da Vittorio il 26 novembre 2026). Chiude i punti
H-2 e H-3.

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
3. Tutto in `/lib/*.d`, nessuna cartella in `/etc`.

**Decisione:** opzione 2.

**Motivazione**
- L'opzione 1 è la cascata che C-3 vieta: due livelli, di cui uno prevale
  sull'altro, e i default fuori da `/etc`.
- L'opzione 3 non ha cascata, ma regge solo se un file di servizio non è
  considerato configurazione. Lo è: contiene argomenti del comando,
  dipendenze, riavvio automatico, destinazione dei log. Inoltre le modifiche
  dell'amministratore verrebbero sovrascritte da apk a ogni aggiornamento e
  non sarebbero coperte da git.
- L'opzione 2 è coerente con C-1 e C-3 e con il criterio di accettazione della
  fase 4 (`ls /etc/dinit.d/` mostra tutti i servizi).
- Un solo posto da guardare per sapere cosa parte all'avvio.
- Il rischio dell'opzione 2, cioè perdere le proprie modifiche a un
  aggiornamento, è coperto due volte: apk non sovrascrive i file di `/etc`
  modificati, e `/etc` è sotto git (C-4).

**Conseguenze**
- In cbuild, con il layout senza `/usr`, i percorsi `usr/lib/<cartella>` delle
  sette cartelle elencate vengono portati in `etc/<cartella>` e il lint non le
  rifiuta più in `/etc`. Fatto sul branch `nonux` di cports e verificato con un
  pacchetto di prova: servizio in `/etc/dinit.d`, abilitazione in
  `/etc/dinit.d/boot.d`, `tmpfiles`, `sysusers` e `sysctl` in `/etc`.
- I link di abilitazione predefinita dei pacchetti finiscono in
  `/etc/dinit.d/boot.d`, la stessa cartella in cui l'amministratore abilita i
  servizi: disabilitare un servizio significa cancellare un file di un
  pacchetto. Da regolare nella guida di stile (fase 5).
- Restano fuori dalla decisione altre cartelle con lo stesso schema, che cbuild
  oggi vuole in `/usr/lib`: `pam.d`, `udev/rules.d`, `udev/hwdb.d`, `kernel.d`.
  Da decidere quando si portano quei pacchetti.
- dinit, `sd-tools` e gli helper di `dinit-chimera` vanno configurati per
  leggere una sola cartella.
- Se un pacchetto aggiorna un servizio che l'amministratore ha modificato, apk
  lascia un file `.apk-new` da confrontare a mano: serve una regola nella
  guida di stile (fase 5).

### D-18b — Avvio: servizi nostri, shell solo come eccezione documentata

**Stato:** presa (Vittorio, 26 novembre 2026). Sostituisce la proposta
precedente ("spostare i percorsi ora, convertire in fase 4").

**Contesto.** `dinit-chimera` (letto al commit `e7e37f5`) contiene 36 script
shell per circa 790 righe, 13 programmi di supporto in C++ per circa 5300
righe, 55 file di servizio, uno script `init` di 81 righe e uno di
spegnimento di 34. Gli script sono di tre tipi:

| Tipo | Quanti | Destino |
|------|--------|---------|
| Funzioni escluse (kdump, cryptsetup, zram, btrfs, ZFS, dmraid, binfmt, conteggio degli avvii) | 9 script, 213 righe | Si tolgono (D-19, D-20, D-21, D-22) |
| Involucri che impostano l'ambiente e lanciano un programma C++ | almeno 11 | Il servizio chiama direttamente il programma |
| Logica vera (fsck, tmpfs, machine-id, LVM, RAID, hostname, …) | una quindicina, circa 450 righe | Vedi sotto |

**Opzioni:** (A) tenere gli script spostando i percorsi; (B) servizi diretti,
shell solo dove c'è logica vera; (C) zero shell, con la logica in un programma
compilato.

**Decisione**
1. **Opzione B, per ora.** I servizi chiamano direttamente i programmi. Uno
   script shell è ammesso solo dove serve logica che un file di servizio non sa
   esprimere, ed è un'eccezione documentata. L'opzione C resta un obiettivo
   successivo.
2. **Niente opzioni di ripristino dalla riga di comando del kernel**
   (`fastboot`, `forcefsck`, `fsck.mode`, `fsck.repair`, `dinit_skip_volumes`).
3. **Pacchetto nostro.** I servizi stanno nella cartella `services/` di questo
   repository e vengono impacchettati a parte. `dinit-chimera` si compila
   senza modifiche e se ne usano solo i programmi di supporto: non si mantiene
   un fork dei suoi servizi.
4. **In fase 2, non in fase 4.** La fase 2 del piano prevede già di scrivere i
   servizi di base; adattare gli script di Chimera per poi sostituirli sarebbe
   lavoro sprecato.

**Si toglie anche** la logica di portabilità che su un sistema noto non serve:
controlli "se il programma non è installato esci", rilevamento dei container,
percorsi alternativi dei file di configurazione.

**Conseguenze**
- A-1 è rispettato con eccezioni elencate. L'elenco delle eccezioni va tenuto
  in `services/` accanto agli script, ognuna con il motivo.
- Senza le opzioni da riga di comando, per saltare o forzare un controllo del
  filesystem bisogna avviare un altro sistema o modificare la configurazione.
- La fase 2 si allarga e somma toolchain nuova e avvio nuovo. Mitigazione: i
  servizi non dipendono dal layout, quindi si sviluppano e si provano su una
  Chimera normale in macchina virtuale, in parallelo alla fase 1.
- La fase 4 si riduce: restano rete, firewall, log, scheduler, dispositivi.
- Il pacchetto dei servizi dipende dai programmi di `dinit-chimera`: a ogni
  sincronizzazione va controllato che i loro argomenti non siano cambiati.

**Da verificare**
- Se lo script `init` si può eliminare facendo partire dinit direttamente dal
  kernel.
- Quali script di logica vera restano come eccezioni: sono stati letti per
  intero solo `root-fsck`, `lvm`, `mdadm`, `hostname`, `fs-fstab`, `tmpfiles`.

---

## D-19 — Nessuna cifratura del disco

**Stato:** presa (Vittorio, 26 novembre 2026).

**Opzioni:** radice cifrata, solo `/home` cifrata, nessuna cifratura.

**Decisione:** nessuna cifratura.

**Motivazione:** la radice cifrata impone un initramfs che chieda la
passphrase, e quello di Chimera (`initramfs-tools`, `cryptsetup-scripts`) è
fatto di script shell. Senza cifratura l'avvio è più semplice e il sistema
minimo ha meno pacchetti.

**Conseguenze**
- Chi ha accesso fisico al disco legge tutto, comprese le password Wi-Fi
  salvate da iwd e le chiavi host di SSH.
- `cryptsetup` e i relativi servizi di avvio di `dinit-chimera` non entrano nel
  sistema.

**Quando rivederla:** se la distro viene installata su un portatile.

---

## D-20 — Volumi: LVM e RAID software sì, zram e kdump no

**Stato:** presa (Vittorio, 26 novembre 2026).

**Decisione:** il sistema supporta LVM e RAID software (`mdadm`). Non supporta
zram né kdump.

**Conseguenze**
- Entrano nel sistema `lvm2` e `mdadm` con i loro servizi di avvio. `lvm2` è
  tra i pacchetti più costosi dell'inventario (51 righe con `usr`).
- I servizi di avvio per LVM e RAID si riscrivono come servizi nostri in
  fase 2 (D-18b); quelli di `dinit-chimera` per cryptsetup, zram e kdump si
  tolgono.
- Lo swap, se serve, è una partizione o un volume normale.
- LVM e RAID si usano per `/home`, `/var` e i dati, non per la radice: vedi D-22.

---

## D-21 — Filesystem ext4, nessuno snapshot

**Stato:** presa (Vittorio, 26 novembre 2026).

**Opzioni:** ext4 con i due meccanismi di ripristino del piano; btrfs con uno
snapshot prima di ogni aggiornamento.

**Decisione:** ext4, nessuno snapshot.

**Motivazione:** gli snapshot non sostituiscono git su `/etc` (C-4), quindi i
meccanismi di ripristino diventerebbero tre; richiedono btrfs e uno strumento
da scrivere e mantenere.

**Conseguenze**
- Il ripristino resta quello del piano: rollback di `/etc` con git e avvio di
  una UKI precedente.
- Un aggiornamento di pacchetti andato male si annulla reinstallando le
  versioni precedenti: va tenuta la cache di apk.
- Con LVM (D-20) restano possibili gli snapshot di volume, come strumento
  manuale e non come parte della procedura di aggiornamento.

**Quando rivederla:** dopo la fase 7. Passare a btrfs richiede una
reinstallazione.

---

## D-22 — Nessun initramfs, radice su partizione semplice

**Stato:** presa (Vittorio, 26 novembre 2026).

**Opzioni:** radice su partizione semplice senza initramfs; radice su LVM o
RAID con initramfs.

**Decisione:** la radice sta su una partizione semplice (ext4, D-21) e il
kernel la monta da solo. Non esiste un initramfs. LVM e RAID (D-20) vengono
attivati dai servizi dinit dopo l'avvio e si usano per `/home`, `/var` e i
dati.

**Motivazione:** senza cifratura (D-19) niente obbliga ad avere un initramfs,
e quello di Chimera è fatto di script shell (`initramfs-tools`, 57 righe con
`usr` nell'inventario), contro A-1. Toglierlo elimina un pacchetto, un
generatore e un passaggio dell'avvio.

**Conseguenze**
- Serve una configurazione del kernel nostra, diversa da quella di Chimera: i
  driver di archiviazione e ext4 vanno compilati dentro il kernel, non come
  moduli. Si includono i driver comuni (NVMe, SATA/AHCI, virtio, archiviazione
  USB), non solo quelli di una macchina: lo stesso kernel serve la macchina
  virtuale e l'hardware reale, e cambiare disco non richiede di ricompilarlo.
- I driver di LVM e RAID possono restare moduli: servono solo dopo il montaggio
  della radice.
- **Microcodice della CPU: scelta rinviata a D-16 (fase 4).** Le strade sono
  tre: (a) un archivio separato che contiene solo il file del microcodice,
  senza script né programmi, che il kernel riceve come initrd; (b) il
  microcodice incluso nel kernel, da ricompilare a ogni aggiornamento; (c) non
  caricarlo e affidarsi al firmware della scheda madre. La preferita è (a), ma
  dipende da come si avvia il kernel e si può verificare solo su hardware
  reale: in macchina virtuale il microcodice non si carica.
- **Vincolo per la fase 2:** la configurazione del kernel tiene attivo il
  supporto agli archivi caricati all'avvio (`CONFIG_BLK_DEV_INITRD`), anche se
  non esiste un initramfs, per non chiudere la strada (a).
- Non c'è una shell di emergenza: se la radice non si monta il kernel si ferma
  e per riparare serve un supporto di avvio esterno.
- L'ibernazione funziona solo con una partizione di swap semplice: il kernel
  da solo non riprende da uno swap su volume LVM o su RAID software.
- I percorsi predefiniti del kernel verso `/sbin` (`modprobe`, spegnimento) si
  fissano nella stessa configurazione o via `sysctl` (vedi `hier.md`).
- La UKI (D-16) contiene kernel e riga di comando, con la radice indicata per
  `PARTUUID`, più l'eventuale archivio del microcodice (strada a).
- La radice non può essere ridimensionata con LVM né avere ridondanza RAID.
- `/var` su un volume separato deve essere montata presto: i servizi che
  scrivono log o stato dipendono dal suo mount.
- I pacchetti `initramfs-tools` e gli hook `install_initramfs` dei template
  non si usano.

**Quando rivederla:** se serve la radice cifrata o ridondante, oppure
l'ibernazione con lo swap su LVM o RAID. Un'alternativa da valutare in quel caso è un
initramfs minimo nostro, con un solo programma e senza shell.

---

## Punti minori del layout

Punti di `hier.md` non coperti sopra. Tutti confermati da Vittorio il 26
novembre 2026, tranne H-7 che è un obiettivo con decisione rinviata.

| Punto | Decisione | Motivazione |
|-------|--------------------|-------------|
| H-1 cartelle temporanee | **Presa:** `/tmp` in RAM, `/var/tmp` vietata | Una sola cartella, niente da pulire. I programmi con temporanei grandi usano `TMPDIR`; quelli con `/var/tmp` nel codice vanno corretti. |
| H-4 sysroot cross | **Presa:** non impacchettare i cross-compilatori | Il piano prevede solo x86_64: senza quei pacchetti la domanda non si pone. |
| H-5 home dei servizi | **Presa:** `/var/lib/<servizio>` | È già "stato dei servizi" secondo `hier.md`. |
| H-6 licenze | **Presa:** `/share/licenses/<pacchetto>` | Come Chimera, senza `/usr`. |
| H-7 LLVM | **Obiettivo:** una sola versione, installata direttamente in `/bin` e `/lib`. Decisione rinviata alla fase 1 | Evita l'eccezione a L-1. Se il costo sul template di `llvm` è troppo alto, si ripiega su `/lib/llvm<N>/` come eccezione documentata. `llvm-bootstrap` resta in una cartella propria, solo sulle macchine di build. |
