#!/bin/sh
# Verifica che la macchina abbia quello che serve per compilare e provare
# Nonux (fase 0, step 6). Non modifica nulla.
#
# Uso: image/check-host.sh [CARTELLA_DI_LAVORO]
# La cartella di lavoro è quella in cui si controlla lo spazio libero
# (predefinita: la cartella corrente).

workdir=${1:-.}
fail=0
warn=0

ok()   { printf '  ok      %s\n' "$1"; }
bad()  { printf '  MANCA   %s\n' "$1"; fail=$((fail + 1)); }
note() { printf '  avviso  %s\n' "$1"; warn=$((warn + 1)); }

have() { command -v "$1" >/dev/null 2>&1; }

need() {
    # need COMANDO DESCRIZIONE
    if have "$1"; then ok "$2 ($1)"; else bad "$2 ($1)"; fi
}

echo "Sistema"
if [ "$(uname -s)" = Linux ] && [ "$(uname -m)" = x86_64 ]; then
    ok "Linux x86_64"
else
    bad "Linux x86_64 (trovato: $(uname -s) $(uname -m))"
fi
if [ "$(id -u)" -ne 0 ]; then
    ok "utente non root (cbuild non gira da root)"
else
    bad "utente non root: cbuild non gira da root"
fi

mem_kb=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo 2>/dev/null)
cpus=$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)
if [ -n "$mem_kb" ]; then
    mem_gb=$((mem_kb / 1024 / 1024))
    if [ "$mem_kb" -ge $((cpus * 2 * 1024 * 1024)) ]; then
        ok "memoria: ${mem_gb} GB per ${cpus} thread"
    else
        note "memoria: ${mem_gb} GB per ${cpus} thread (cbuild consiglia 2 GB per thread: ridurre i job)"
    fi
fi

free_kb=$(df -Pk "$workdir" 2>/dev/null | awk 'NR == 2 {print $4}')
if [ -n "$free_kb" ]; then
    free_gb=$((free_kb / 1024 / 1024))
    if [ "$free_gb" -ge 100 ]; then
        ok "spazio libero in $workdir: ${free_gb} GB"
    else
        bad "spazio libero in $workdir: ${free_gb} GB (servono almeno 100 GB)"
    fi
else
    bad "impossibile leggere lo spazio libero in $workdir"
fi

echo "Compilazione dei pacchetti (cbuild)"
need git "git"
need bwrap "bubblewrap"
need openssl "openssl (generazione delle chiavi)"
if have python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 12))'; then
    ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
else
    bad "Python 3.12 o successivo"
fi
if have apk && apk --version 2>/dev/null | grep -q 'apk-tools 3'; then
    ok "apk-tools 3 ($(command -v apk))"
else
    bad "apk-tools 3 (binario statico: https://repo.chimera-linux.org/apk/latest/)"
fi
if have ruff || { have flake8 && have black; }; then
    ok "linter e formatter Python (ruff, oppure flake8 e black)"
else
    bad "linter e formatter Python (ruff, oppure flake8 e black)"
fi
if have bwrap && bwrap --unshare-all --ro-bind / / true 2>/dev/null; then
    ok "namespace utente utilizzabili da bubblewrap"
else
    bad "namespace utente: bwrap non riesce a creare un ambiente isolato"
fi

echo "Macchina virtuale"
if [ -c /dev/kvm ]; then
    if [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
        ok "KVM accessibile"
    else
        bad "KVM presente ma non accessibile (aggiungere l'utente al gruppo kvm)"
    fi
else
    bad "KVM (/dev/kvm non esiste: virtualizzazione disattivata o modulo non caricato)"
fi
need qemu-system-x86_64 "QEMU"
need qemu-img "qemu-img"
ovmf=
for f in \
    /usr/share/OVMF/OVMF_CODE.fd \
    /usr/share/OVMF/OVMF_CODE_4M.fd \
    /usr/share/edk2/ovmf/OVMF_CODE.fd \
    /usr/share/edk2/x64/OVMF_CODE.4m.fd \
    /usr/share/edk2-ovmf/x64/OVMF_CODE.fd \
    /usr/share/qemu/OVMF.fd \
    /usr/share/ovmf/OVMF.fd
do
    [ -r "$f" ] && ovmf=$f && break
done
if [ -n "$ovmf" ]; then
    ok "firmware EFI: $ovmf"
else
    bad "firmware EFI OVMF (pacchetto ovmf o edk2-ovmf)"
fi

echo "Documentazione e test"
need mandoc "mandoc"
if have python3 && python3 -c 'import pytest' 2>/dev/null; then
    ok "pytest"
else
    bad "pytest"
fi

echo
if [ "$fail" -eq 0 ]; then
    echo "Tutto presente (avvisi: $warn)."
else
    echo "Mancano $fail requisiti (avvisi: $warn)."
fi
[ "$fail" -eq 0 ]
