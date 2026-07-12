# cesco.it — sito web personale

Sito statico personale di Francesco Maida (promozione servizi di consulenza
informatica a Venezia). Generato con **Flask + Frozen-Flask** appoggiandosi
alla libreria **sitekit** (repo separato, installata via git da GitHub).

## Stack e comandi

- **Python** ≥ 3.12, dipendenze gestite con **Poetry**
- `poetry run serve` — server di sviluppo Flask (debug) su localhost
- `poetry run build` — freeze del sito statico in `~/Sites/cesco.it`
  (BUILD_DIR impostato in `src/tools/build.py`)
- Hosting di produzione: VPS OVH. Il file `netlify.toml` è un residuo di un
  vecchio esperimento di deploy su Netlify: la sua `publish = "build"` NON è
  coerente con il BUILD_DIR reale.

## Struttura

| Percorso | Contenuto |
|---|---|
| `src/main/app.py` | App Flask: route `/`, `/privacy/`, handler 404 |
| `src/tools/build.py` | Script di freeze + sitemap + robots.txt |
| `src/tools/serve.py` | Avvio del server di sviluppo |
| `content/*/_config.yaml` | Contenuti a sezioni (projects, services, plans, answers, examples, privacy) |
| `content/blog/` | Page-bundle markdown NON più usati in homepage (vedi Blog) |
| `templates/` | Template Jinja2 (tema "Bolby" adattato) |
| `templates/_default/baseof.html` | Layout base; definisce `{% block title %}` |
| `templates/partials/head.html` | Meta tag, SEO, JSON-LD, CSS |
| `templates/partials/home/*.html` | Sezioni della one-page, incluse da `index.html` |
| `static/` | Asset del tema + immagini generate in `static/cache/` |
| `i18n/it.json` | Stringhe di traduzione (chiavi in inglese) |

## Convenzioni importanti

- **Titoli pagina**: `baseof.html` contiene
  `<title>{% block title %}{{ params.title }}{% endblock %}</title>`;
  ogni template di pagina sovrascrive `{% block title %}`. Non rimettere un
  `<title>` fisso dentro `head.html`.
- **Chiave `base-url`**: in `content/_config.yaml` si chiama `base-url`
  (con trattino). Nei template va letta come `params['base-url']` — mai con
  spazi nella chiave (un refuso `params[" base-url"]` ha già causato
  canonical e og:url vuoti in produzione). Canonical e og:url sono per-pagina:
  `{{ params['base-url'] ~ request.path }}`.
- **Immagini**: generate da `sitekit.images.copy()` nei 4 breakpoint
  400/800/1200/1600 px (AVIF/WebP/JPEG) dentro `static/cache/<sezione>/`.
  L'aspect ratio dei progetti dipende dal tag: `siti_web` → 1:2 (anchor top),
  `documenti` → 2:3, `app` → 16:9, default 1:1. La stessa logica esiste sia
  in `app.py` (render) sia in `build.py` (pregenerazione): se si cambia una,
  aggiornare anche l'altra.
- **Tag dei progetti**: minuscoli con underscore (es. `siti_web`); i template
  li mostrano con `| replace("_", " ") | title`.
- **Blog**: la homepage mostra i post scaricati da Memos
  (`https://memos.cesco.it`, tag `#lavoro`) tramite la libreria
  `grabmymemos`; il token sta in `~/.config/cesco.it/memos.token` (fuori dal
  repo). Il download è protetto da try/except: se Memos è irraggiungibile la
  build procede con lista post vuota. I page-bundle in `content/blog/` sono
  il vecchio meccanismo, ancora pre-generati da `build.py` ma non mostrati.
- **Form contatti**: backend **Formcarry** (action nel form di
  `9-contact.html`) + Cloudflare **Turnstile**. Niente JavaScript custom di
  invio: submit nativo del form. I vecchi `contact.js` (Formspree) e
  `contact.php` sono stati dismessi.
- **404**: l'error handler restituisce status 404; per questo `build.py`
  imposta `FREEZER_IGNORE_404_NOT_FOUND = True` (la pagina `/404.html` viene
  generata comunque). Non rimuovere quell'opzione.
- **Freeze**: un errore durante `freezer.freeze()` termina la build con
  `sys.exit(1)` senza eseguire la pulizia cache. Non silenziare le eccezioni.
- **i18n**: `i18n/it.json` non deve contenere chiavi duplicate.

## SEO

- `head.html` genera meta description, Open Graph, canonical e JSON-LD
  (schema.org `Person` con `knowsAbout` ricavato dai servizi).
- `build.py` genera `sitemap.xml` (via `sitekit.sitemap`) e `robots.txt`
  (via `sitekit.robots`) dentro BUILD_DIR a fine freeze.
- Favicon: `static/images/logo.svg` referenziato come `rel="icon"`.

## Test

Il progetto non ha ancora una suite di test propria (`tests/` è vuota);
la libreria sitekit ha la sua suite (`pytest` dalla root di sitekit).

## Metadata
- Ultima modifica: 2026-07-12
- Modello: claude-fable-5
