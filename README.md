# Il mio sito web personale

Sito statico bilingue (italiano/inglese) generato con [Hugo](https://gohugo.io)
(versione 0.146 o successiva).

- `hugo server` avvia il sito in locale su http://localhost:1313 con
  ricaricamento automatico.
- `python3 build.py` compila il sito nella cartella `publishDir` di
  `config/_default/hugo.yaml` (oggi `/Users/cesco/Sites/cesco.it`), eseguendo
  prima e dopo la build i comandi elencati nelle liste `pre` e `post` di
  `build.toml`. Richiede Python 3.11
  o successivo, senza dipendenze esterne. Opzioni: `--dest <cartella>`,
  `--config <file.toml>`, `--skip-hooks`.

Dove modificare cosa:

- configurazione e testi generali: `config/_default/`
- pagine, servizi, portfolio, laboratorio, blog: `content/`
- curriculum, piani, esempi, "perché scegliere me": `data/it/` e `data/en/`
- traduzioni dell'interfaccia: `i18n/`
