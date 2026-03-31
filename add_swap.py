
"""
Erstellt eine 16GB Swap-Datei und aktiviert sie.
Muss mit sudo ausgeführt werden: sudo python3 add_swap.py

HINWEIS: Funktioniert nur auf Linux.
"""

import shutil
import subprocess
import sys
import os
import platform

SWAP_SIZE_GB = 16
MAX_SWAP_GB = 64  # Sicherheitslimit
SWAP_FILE = "/swapfile_extra"


def run(cmd, check=True):
    print(f"  → {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  FEHLER: {result.stderr.strip()}")
        sys.exit(1)
    return result


def main():
    if platform.system() != "Linux":
        print("FEHLER: Dieses Skript funktioniert nur auf Linux.")
        print("macOS verwaltet Swap automatisch unter /private/var/vm/")
        sys.exit(1)

    if os.geteuid() != 0:
        print("FEHLER: Bitte mit sudo ausführen:")
        print(f"  sudo python3 {sys.argv[0]}")
        sys.exit(1)

    if os.path.exists(SWAP_FILE):
        print(f"FEHLER: {SWAP_FILE} existiert bereits.")
        print(f"  Zum Entfernen: sudo swapoff {SWAP_FILE} && sudo rm {SWAP_FILE}")
        sys.exit(1)

    # Sicherheitsprüfungen
    if SWAP_SIZE_GB > MAX_SWAP_GB:
        print(f"FEHLER: {SWAP_SIZE_GB}GB überschreitet das Sicherheitslimit von {MAX_SWAP_GB}GB.")
        sys.exit(1)

    free_gb = shutil.disk_usage("/").free / (1024 ** 3)
    if SWAP_SIZE_GB >= free_gb * 0.9:
        print(f"FEHLER: Nicht genug Speicherplatz. {free_gb:.1f}GB frei, {SWAP_SIZE_GB}GB angefordert.")
        print("  Es müssen mindestens 10% freier Platz übrig bleiben.")
        sys.exit(1)

    print(f"=== Erstelle {SWAP_SIZE_GB}GB Swap-Datei: {SWAP_FILE} ===\n")

    # 1. Swap-Datei erstellen
    print(f"[1/4] Erstelle {SWAP_SIZE_GB}GB Datei (das dauert etwas)...")
    run(["fallocate", "-l", f"{SWAP_SIZE_GB}G", SWAP_FILE])

    # 2. Berechtigungen setzen (nur root darf lesen/schreiben)
    print("[2/4] Setze Berechtigungen (600)...")
    os.chmod(SWAP_FILE, 0o600)

    # 3. Als Swap formatieren
    print("[3/4] Formatiere als Swap...")
    run(["mkswap", SWAP_FILE])

    # 4. Swap aktivieren
    print("[4/5] Aktiviere Swap...")
    run(["swapon", SWAP_FILE])

    # 5. In /etc/fstab eintragen für Permanenz
    fstab_line = f"{SWAP_FILE}  none  swap  sw  0  0"
    print("[5/5] Trage Swap in /etc/fstab ein (permanent)...")
    with open("/etc/fstab", "r") as f:
        fstab_content = f.read()
    if SWAP_FILE not in fstab_content:
        with open("/etc/fstab", "a") as f:
            f.write(f"\n{fstab_line}\n")
        print(f"  → Eintrag hinzugefügt: {fstab_line}")
    else:
        print(f"  → Eintrag existiert bereits in /etc/fstab")

    print(f"\n=== Fertig! {SWAP_SIZE_GB}GB Swap wurde permanent aktiviert. ===")
    print()

    # Status anzeigen
    print("Aktueller Swap-Status:")
    run(["swapon", "--show"])

    print(f"\nZum Entfernen:")
    print(f"  sudo swapoff {SWAP_FILE}")
    print(f"  sudo rm {SWAP_FILE}")
    print(f"  Und den Eintrag aus /etc/fstab entfernen.")


if __name__ == "__main__":
    main()
