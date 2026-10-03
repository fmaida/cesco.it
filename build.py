#!/usr/bin/env python3
"""
Build del sito cesco.it con Hugo.

Esegue, nell'ordine:
  1. i comandi "pre" di build.toml (es. scaricare i post del blog);
  2. hugo, con gli argomenti di "hugo_args", scrivendo il sito nella cartella
     "publishDir" di config/_default/hugo.yaml (o in "destination"/--dest);
  3. i comandi "post" (es. pubblicare il sito sul VPS con rsync).

I comandi passano dalla shell e partono dalla cartella del progetto. Possono
usare il segnaposto {destination} e trovano la cartella di destinazione anche
nella variabile d'ambiente BUILD_DIR. Al primo comando che fallisce lo script
si ferma con lo stesso exit code: i comandi "post" partono solo se la build
di Hugo è riuscita.

Uso:
    python3 build.py                    # usa build.toml
    python3 build.py --dest /tmp/sito   # cambia la cartella di destinazione
    python3 build.py --skip-hooks       # solo Hugo, senza comandi pre/post
    python3 build.py --config altro.toml

Richiede Python 3.11 o successivo (tomllib) e hugo nel PATH.
"""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

PROGETTO = Path(__file__).resolve().parent


def carica_config(percorso: Path) -> dict:
    """Legge il file toml di configurazione della build e ne controlla i campi."""

    if not percorso.exists():
        sys.exit(f"❌ File di configurazione non trovato: {percorso}")

    with percorso.open("rb") as file:
        config = tomllib.load(file)

    for chiave in ("hugo_args", "pre", "post"):
        valore = config.setdefault(chiave, [])
        if not isinstance(valore, list) or not all(isinstance(v, str) for v in valore):
            sys.exit(f"❌ In {percorso.name}, \"{chiave}\" deve essere una lista di stringhe")

    if "destination" in config and not isinstance(config["destination"], str):
        sys.exit(f"❌ In {percorso.name}, \"destination\" deve essere un percorso")

    return config


def publish_dir_di_hugo(hugo: str) -> str:
    """La cartella "publishDir" della configurazione di Hugo (config/_default/hugo.yaml)."""

    esito = subprocess.run([hugo, "config", "--format", "json"], cwd=PROGETTO,
                           capture_output=True, text=True)
    if esito.returncode != 0:
        sys.exit(f"❌ Impossibile leggere la configurazione di Hugo:\n{esito.stderr}")

    return json.loads(esito.stdout)["publishdir"]


def esegui(comando: str | list[str], ambiente: dict, shell: bool) -> None:
    """Esegue un comando dalla cartella del progetto; se fallisce, termina lo script."""

    testo = comando if isinstance(comando, str) else shlex.join(comando)
    print(f"▶ {testo}", flush=True)
    esito = subprocess.run(comando, cwd=PROGETTO, env=ambiente, shell=shell)
    if esito.returncode != 0:
        print(f"❌ Comando fallito (exit code {esito.returncode}): {testo}", file=sys.stderr)
        sys.exit(esito.returncode)


def esegui_fase(nome: str, comandi: list[str], destinazione: Path, ambiente: dict) -> None:
    """Esegue i comandi di una fase ("pre" o "post"), sostituendo {destination}."""

    if not comandi:
        return

    print(f"\n— Comandi {nome} —")
    for comando in comandi:
        esegui(comando.replace("{destination}", str(destinazione)), ambiente, shell=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compila il sito con Hugo, con comandi prima e dopo la build.")
    parser.add_argument("--config", type=Path, default=PROGETTO / "build.toml",
                        help="file di configurazione (predefinito: build.toml)")
    parser.add_argument("--dest", help="cartella di destinazione (sovrascrive publishDir di Hugo e \"destination\" di build.toml)")
    parser.add_argument("--skip-hooks", action="store_true", help="non eseguire i comandi pre e post")
    argomenti = parser.parse_args()

    config = carica_config(argomenti.config)

    hugo = shutil.which("hugo")
    if hugo is None:
        sys.exit("❌ hugo non trovato nel PATH: installalo con \"brew install hugo\"")

    # Destinazione: --dest, poi "destination" di build.toml, poi publishDir di Hugo
    scelta = argomenti.dest or config.get("destination") or publish_dir_di_hugo(hugo)
    destinazione = (PROGETTO / Path(os.path.expandvars(scelta)).expanduser()).resolve()

    # Con --cleanDestinationDir Hugo cancella dalla destinazione tutto ciò che
    # non appartiene al sito: un refuso nel percorso non deve svuotare la home
    if destinazione in (Path("/"), Path.home().resolve(), PROGETTO) or PROGETTO.is_relative_to(destinazione):
        sys.exit(f"❌ Destinazione non valida: {destinazione}")

    ambiente = dict(os.environ, BUILD_DIR=str(destinazione))

    if not argomenti.skip_hooks:
        esegui_fase("pre", config["pre"], destinazione, ambiente)

    print("\n— Build di Hugo —")
    esegui([hugo, *config["hugo_args"], "--destination", str(destinazione)], ambiente, shell=False)

    if not argomenti.skip_hooks:
        esegui_fase("post", config["post"], destinazione, ambiente)

    print(f"\n✅ Sito pronto in {destinazione}")


if __name__ == "__main__":
    main()
