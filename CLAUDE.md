# cesco.it — sito web personale

Sito statico personale di Francesco Maida (promozione servizi di consulenza
informatica a Venezia), **multi-pagina e bilingue** (italiano alla radice,
inglese sotto `/en/`). Generato con **Hugo** (≥ 0.146, nuovo sistema di
template; sviluppato con 0.167). Fino a ottobre 2026 era un progetto
Flask + Frozen-Flask + sitekit: quel codice non c'è più.

**Francesco detesta i Go template.** La logica sta in pochi partial
commentati in italiano; il lavoro di tutti i giorni (testi, voci, prezzi,
traduzioni) si fa in markdown, YAML e JSON senza toccare `layouts/`.
Quando aggiungi funzionalità, mantieni questa separazione.

## Comandi

- `hugo server` — server di sviluppo su http://localhost:1313
  (configurazione `cesco-serve` in `.claude/launch.json`)
- `python3 build.py` — build nella cartella `publishDir` di
  `config/_default/hugo.yaml` (`/Users/cesco/Sites/cesco.it`, percorso
  assoluto perché Hugo non espande `~`), con le opzioni di `build.toml`:
  esegue i comandi `pre`, poi `hugo --gc --cleanDestinationDir`, poi
  i comandi `post`. Opzioni: `--dest`, `--config`, `--skip-hooks`. Solo
  libreria standard (Python ≥ 3.11). Al primo comando che fallisce si ferma
  con lo stesso exit code; i `post` partono solo se Hugo è riuscito.
  Rifiuta destinazioni pericolose (/, home, cartella del progetto).
- **Minificazione** sempre attiva, anche con `hugo` da solo e `hugo server`:
  blocco `minify` di `hugo.yaml` (`minifyOutput: true` per HTML, XML, JSON,
  SVG; opzioni tdewolff al massimo senza perdita, che valgono anche per il
  pipe `minify` di CSS e JS). L'HTML perde tag di chiusura facoltativi,
  virgolette e valori predefiniti degli attributi (es. `type="text"`): nel
  CSS e nel JS non selezionare elementi con `[type=text]` e simili, usa
  classi o `data-*`. `css.version`/`js.version: 0` = versione più recente
  (in Hugo ≥ 0.150 `keepCSS2` non esiste più).
- **Attenzione**: `hugo` da solo scrive direttamente nella cartella di deploy
  (`publishDir`). Per le prove usa `hugo server` (lavora in memoria) oppure
  `hugo -d <cartella temporanea>`.
- Hosting di produzione: VPS OVH con Caddy (vedi sezione "Caddy").

## Struttura

| Percorso | Contenuto |
|---|---|
| `config/_default/hugo.yaml` | Impostazioni generali (baseURL, lingua predefinita, output, sitemap, robots, immagini, minificazione) |
| `config/_default/languages.yaml` | Lingue, permalink per lingua e testi tradotti in `<lingua>.params` (descrizione, promessa della home, testo contatti) |
| `config/_default/params.yaml` | Dati comuni: contatti, tariffe, autore (avatar, cv), social, identità nel fediverso e su Bluesky (`fediverse`, `bluesky`), codici QR corti (`qr`), dati fiscali, lato della sidebar (`layout.sidebar`), accenti del tema, Formcarry/Turnstile, Umami |
| `config/_default/menus.{it,en}.yaml` | Barra laterale e ordine delle frecce prev/next (`name` = chiave i18n, `params.icon`) |
| `config/_default/markup.yaml` | Goldmark con `unsafe: true` (i testi contengono HTML) |
| `config/development/params.yaml` | Valori solo per `hugo server`: Turnstile di prova e invio simulato del modulo |
| `content/` | Pagine: `_index.md` (home), `about.md` (tutto il testo di Chi sono), `contact.md`, `privacy.md` (+ `.en.md`), le sezioni `services/`, `portfolio/`, `lab/`, `blog/` e `llms/` (testo di `llms.txt`, senza pagina HTML) |
| `i18n/{it,en}.json` | Stringhe di interfaccia (formato piatto chiave → testo, stesse chiavi nei due file) |
| `layouts/` | Template: `baseof`, `home`, `about`, `contact`, `privacy`, `404`, `section` (griglia delle collezioni), `page` (dettaglio voce), `blog/` (elenco, post, feed RSS), `robots.txt`, e i file senza estensione della home: `home.webfinger`, `home.atproto-did`, `home.caddy` (vedi "Caddy") e `home.llms.txt` (vedi "SEO") |
| `layouts/_partials/` | `head`, `header`, `footer`, `arrows` e gli helper (vedi sotto) |
| `layouts/_markup/` | Render hook delle immagini nel markdown: `render-image.html` (`<picture>`) e `render-image.rss.xml` (un `<img>` assoluto per il feed) |
| `layouts/_shortcodes/` | `dato` (`{{< dato "chiave" >}}`: un dato del front matter o dei params nel testo di una pagina), `itchio` (`{{< itchio iframe="https://itch.io/embed/<id>" src="<pagina del gioco>" title="…" >}}`: widget di un gioco su itch.io, 552×167 px), `immagine` (`{{< immagine src="file.jpg" alt="…" didascalia="…" larghezza="400" >}}`: immagine del bundle o di `assets/` al centro della colonna, che al clic si apre in una lightbox, vedi "Immagini"; non è il partial `immagine.html`) e i blocchi grafici della pagina Chi sono (vedi sotto) |
| `assets/site/` | `css/site.css` e `js/site.js` del layout (minificati e con fingerprint) |
| `assets/images/` | Immagini elaborate da Hugo (vedi "Immagini"): `avatar.jpg`, `no-image.jpg` (copertina dei post senza immagine), `answers/` (sezione "Perché scegliere me") |
| `static/` | Copiati così come sono alla radice del sito: logo, icone SVG, favicon, `downloads/cv.pdf`. **Niente immagini raster qui**: non verrebbero convertite |
| `build.py`, `build.toml` | Script di build con comandi pre/post |

Helper in `layouts/_partials/`: `icon` (SVG inline), `immagine` e
`responsive-image` (vedi "Immagini"), `lightbox` (GLightbox per lo shortcode `immagine`),
`project-media`, `offerta` (blocco `offer` delle voci), `aspect` (proporzioni dai tag), `rientro` (toglie
l'indentazione comune al contenuto di uno shortcode, ignorando le righe
vuote), `compatta` (HTML su una riga sola), `testo` (segnaposto
`{{ params.fares.* }}` e `{{ params.support.email }}` nei testi di
`languages.yaml`), `tag` (etichetta tradotta di un tag),
`traduzioni` (URL della pagina in ogni lingua), `sezione-corrente` (voce di
menu attiva), `filtri` (riga di filtri per tag), `blog-italiano`, `copertina` (il valore di `image` di un post).

## Pagine e lingue

| Pagina | IT | EN | File |
|---|---|---|---|
| Home | `/` | `/en/` | `content/_index(.en).md` → `home.html` |
| Chi sono | `/chi-sono/` | `/en/about/` | `content/about(.en).md` (`slug`, `layout: about`) |
| Servizi | `/servizi/` e `/servizi/<slug>/` | `/en/services/…` | `content/services/` |
| Portfolio | `/portfolio/` e `/portfolio/<slug>/` | `/en/portfolio/…` | `content/portfolio/` |
| Laboratorio | `/laboratorio/` e `/laboratorio/<slug>/` | `/en/lab/…` | `content/lab/` |
| Blog | `/blog/` | `/en/blog/` | `content/blog/` |
| Contatti | `/contatti/` | `/en/contacts/` | `content/contact(.en).md` |
| Privacy | `/privacy/` | `/en/privacy/` | `content/privacy(.en).md` |

- Traduzioni **per nome file**: `pagina.md` (italiano) e `pagina.en.md` nella
  stessa cartella. Gli URL diversi tra le lingue vengono da `slug` nelle pagine
  singole e da `permalinks` in `languages.yaml` per le sezioni.
- Per aggiungere una pagina: file in `content/` (+ `.en.md`) con `slug` e
  `layout`, template in `layouts/`, voce in `menus.*.yaml` se va nella sidebar.
- **Indirizzi di 4 caratteri A-Z/2-9 alla radice (`/ab23/`) riservati ai
  codici QR** (vedi "Caddy"): niente pagine, sezioni o slug così, a parte
  `blog`, che c'era già (eccezioni in `$eccezioni` di `layouts/home.caddy`).
  Una pagina così ferma la build.
- Il nome di menu viene da `i18n` (chiave in `menus.*.yaml`); il `title` del
  front matter dà il `<title>` e `og:title`, `description` la meta
  description e `og:description` (vedi "SEO").
- **Titolo grande (h1)**: nelle pagine singole (Chi sono, contatti, privacy) e
  negli `_index.md` delle sezioni (servizi, portfolio, laboratorio, blog) è la
  prima riga del testo: `{{< titolo "Chi <span>Sono</span>" >}}` (la parola
  nello `<span>` prende il colore d'accento). I template non lo stampano più:
  una pagina nuova di questo tipo deve avere lo shortcode, altrimenti resta
  senza h1. Fanno eccezione le voci delle collezioni e i post del blog (h1 dal
  `title`, con il link di ritorno; i post li genera *memos 2 hugo*), la home
  (h1 = la promessa di `slogan`, vedi "Homepage") e la 404 (`title-block`).

## Collezioni (servizi, portfolio, laboratorio)

- Una cartella per voce (page bundle): `content/<sezione>/<slug>/index.md` +
  `index.en.md`, con l'immagine/video accanto. Front matter: `title`, `slug`
  (uguale nelle due lingue), `weight` (ordine nella griglia), `tags`, e
  facoltativi `image` (file del bundle), `icon` (SVG in `static/`, servizi),
  `meta` (voce di `knowsAbout` nel JSON-LD, servizi), `client`, `year`,
  `website` (link "Visita il sito"; **non** `url`, che in Hugo è riservato).
  Il corpo markdown è la descrizione.
- Blocco facoltativo `offer` (`_partials/offerta.html`): `description` e
  `price` in markdown, `cta.title` + `cta.url` (pulsante; percorso del sito o
  URL esterno). Se c'è, accanto alla copertina compaiono descrizione, prezzo
  in un riquadro e pulsante, e il corpo markdown va sotto, a tutta larghezza
  (`.project-body`). Il pulsante dell'offerta prende il posto di "Richiedi un
  preventivo" (`contatto: true`). Esempio: `content/services/001-ottimizzazione-profili-google/`.
- `_index.md` della sezione: `title`, titolo grande (`{{< titolo "…" >}}`) e
  descrizione nel corpo, `filters` (tag
  dei pulsanti filtro), `back` (chiave i18n del link di ritorno),
  `contatto: true` (pulsante "Richiedi un preventivo" e invito sotto la
  griglia), `senza_categoria: true` (niente tag sotto i nomi), `other`
  (servizi: altre voci di `knowsAbout`), `sitemap` e `cascade` (sitemap
  delle voci, `build.publishResources: false` per non pubblicare gli originali).
- Una voce senza `image` mostra la sua `icon` o un segnaposto con l'icona flask.
- **Filtri** (`_partials/filtri.html`, usato da `section.html` e dal blog):
  "Tutto" + un pulsante per tag; agiscono sulle voci con `data-groups` dentro
  il contenitore `data-filtri` (`site.js`). Il filtro attivo diventa scuro.
  Nel blog i filtri si ricavano dai `tags` dei post e la riga compare solo se
  ci sono post con tag.
- **Tag**: minuscoli con underscore (`siti_web`; servizi: `sviluppo`,
  `grafica`, `marketing`); l'etichetta viene da `i18n/*.json` (chiave = tag),
  con ripiego sul tag reso leggibile. Le pagine di tassonomia sono disattivate.
- **Proporzioni** delle immagini dai tag (`_partials/aspect.html`):
  `siti_web` → 1:2 ancorata in alto, `documenti` → 2:3, `app` → 16:9, altrimenti 1:1.
- **Immagini responsive**: vedi la sezione "Immagini".
- Prev/next nel dettaglio: ordine per `weight`. In Hugo `.Next` restituisce la
  voce che viene **prima** nella lista e `.Prev` quella dopo (già gestito in `page.html`).

## Immagini

Ogni immagine raster mostrata dal sito esiste in **AVIF, WebP e nel formato
di ripiego** (PNG se l'originale è PNG, così resta la trasparenza; altrimenti
JPEG), dentro un `<picture>`: il browser prende il primo formato che sa
mostrare e, nel formato, la larghezza giusta da `srcset`/`sizes`.

- **`_partials/immagine.html`** è il punto d'ingresso: riceve un percorso o un
  URL (`src`) e cerca, nell'ordine, l'URL remoto (scaricato con
  `resources.GetRemote` e pubblicato sotto `/images/esterne/`; se non
  risponde: warning e `<img>` verso l'URL), il file del page bundle (`page`),
  `assets/`, e infine `static/` (servito così com'è). SVG e GIF (animate)
  restano un `<img>`. Con `abs: true` dà un solo `<img>` assoluto nel formato
  di ripiego (feed RSS). Usarlo per **ogni** immagine nuova nei template.
- **`_partials/responsive-image.html`** fa le conversioni: `Fill` di Hugo
  (ridimensiona e poi ritaglia) alle proporzioni `w`/`h` (senza: quelle
  dell'originale) a 400/800/1200/1600 px, più la larghezza massima
  dell'originale se sta in mezzo o sotto i 400; mai ingrandimenti, e
  `width`/`height` mai oltre l'originale. **Non usare `Crop`**: ritaglia senza
  ridimensionare e mostra solo un dettaglio dell'immagine. Qualità in
  `hugo.yaml` → `imaging` (jpeg/webp 82, avif 75).
- Mette `style="aspect-ratio:w/h"` sull'`<img>`, che vince sul CSS: se il CSS
  impone un'altra proporzione, passa la stessa in `w`/`h` (es. le copertine
  nell'elenco del blog, 214:100 come `.media-block img`) o usa `!important`.
- `picture { display: contents }` nel CSS: i selettori scritti per `img`
  continuano a valere.
- **Lightbox** (shortcode `immagine`): **GLightbox** (MIT), versione in
  `$versione` di `_partials/lightbox.html`. Hugo scarica CSS e JS da jsDelivr
  al build (`resources.GetRemote`, con la cache) e li pubblica sotto
  `/vendor/glightbox/` con fingerprint: il visitatore non contatta la CDN,
  quindi nell'informativa privacy non c'è. Si caricano solo nelle pagine con
  lo shortcode, che lo segnala con `.Page.Store.Set "lightbox" true`;
  `baseof.html` li mette prima di `site.js`, che avvia la lightbox sui link
  `[data-lightbox]`. Nella lightbox va l'originale (o una versione da 2000 px
  se è più grande), non convertito.
- **Angoli arrotondati** (`--radius-media`, 6px, in `:root` di `site.css`):
  copertine delle griglie, della pagina della voce e delle schede del blog,
  immagini nel testo (`.figura`, `.project-details`, `.prose`), immagine e
  didascalia della lightbox (regole `.glightbox-clean`), riquadro del prezzo
  dell'offerta. Un nuovo elemento di questo tipo usa la stessa variabile.
- Dove si usa: voci delle collezioni (`project-media`), avatar della sidebar,
  copertine e segnaposto del blog, immagini nel markdown (render hook in
  `layouts/_markup/`), `risposta`, `certificato` (`logo=`), `piano`
  (`icona=`), lo shortcode `immagine`. Restano fuori, di proposito: favicon e `og:image`/JSON-LD
  (l'avatar JPEG originale: i social non leggono AVIF/WebP).

## Convenzioni importanti

- **Titoli pagina**: `baseof.html` ha `<title>{{ block "title" . }}`; ogni
  template di pagina definisce `title`. Canonical, og:url e hreflang
  (it/en/x-default) sono per pagina, da `.Permalink` e `.AllTranslations`:
  `hreflang` solo verso le traduzioni che esistono (i post del blog, solo in
  italiano, non ne hanno). Il selettore di lingua invece usa
  `_partials/traduzioni.html`, che ripiega sulla home dell'altra lingua.
- **Linkify** di Goldmark attivo: nel markdown `www.qualcosa.it` e gli
  indirizzi email diventano link da soli. Negli esempi fittizi si evita con
  `\.` (`*www\.azienda\.com*`).
- **Layout**: ricalca BreezyCV (barra icone 80px, colonna profilo 420px color
  accento, contenuto bianco) ma è scritto da zero.
  **Lato della sidebar configurabile** con `layout.sidebar` (`left`/`right`,
  oggi `right`) in `params.yaml`: `baseof.html` lo mette in
  `<html data-sidebar="…">` (valore non valido = errore di build) e il CSS
  ribalta solo le proprietà orizzontali nel blocco
  `:root[data-sidebar="right"]` (e nella media query < 1024px: drawer che
  entra da destra, pulsante menu a sinistra). Le regole base descrivono la
  sidebar a sinistra: se aggiungi regole con left/right, aggiungi anche la
  versione ribaltata. Nessun asset del tema originale, che è a pagamento.
  **Niente Bootstrap, jQuery né Font Awesome**: tutte le icone sono SVG inline da `_partials/icon.html` (linea: Tabler, MIT;
  piene — social, freccia, rss — glifi di Font Awesome Free 5, CC BY 4.0,
  classe `icon-fill`; `bluesky` viene da Font Awesome Free 6, con le y
  ribaltate per usare le stesse coordinate di font degli altri; `substack`, che
  Font Awesome non ha, viene da Simple Icons, CC0, scalata e ribaltata allo
  stesso modo). Font Poppins da Google Fonts. Sotto i 1024px barra e
  colonna diventano un drawer.
  Barra icone e colonna profilo sono `position: fixed`, alte quanto la
  finestra; i loro colori sono dipinti anche sullo sfondo del `body`
  (gradienti ripetuti in verticale, dalle stesse variabili), così negli
  screenshot "pagina intera" la colonna resta colorata per tutta la pagina.
- **Barra di scorrimento** della pagina sempre visibile (`html { overflow-y:
  scroll }` + `html::-webkit-scrollbar` per Chrome/Safari, `scrollbar-color`
  in `@supports` per Firefox) e nei colori del tema (`--scrollbar-thumb`,
  `--scrollbar-track`): così il layout non si sposta tra pagine corte e
  lunghe. Non aggiungere `scrollbar-color` fuori dal `@supports`: in Chrome
  disattiverebbe le regole `::-webkit-scrollbar`.
- **Tema chiaro/scuro**: tre modalità (automatico, chiaro, scuro) dai pulsanti
  nella colonna profilo. Uno script inline in cima a `head.html` imposta su
  `<html>` `data-theme` (`light`/`dark`) e `data-theme-pref`
  (`auto`/`light`/`dark`) prima dei CSS, senza lampeggio. La scelta sta in
  `localStorage["tema"]`; se manca vale "automatico". Gli accenti, uno per tema,
  sono in `params.yaml` (`theme.accent-light`, `theme.accent-dark`).
  **Ogni colore nel CSS va messo in variabile** e, se serve, ridefinito nel
  blocco `:root[data-theme="dark"]`. Turnstile riceve il tema effettivo al
  caricamento della pagina.
- **Frecce prev/next**: scorrono in ciclo le voci di `menus.*.yaml`; una voce
  di collezione conta come la sua sezione; niente frecce su privacy e 404.
  Sono centrate sul bordo esterno del contenuto (lato opposto alla sidebar) e
  non in basso, perché **l'angolo in basso sul lato del contenuto è riservato
  a un futuro widget di supporto** (oggi, con la sidebar a destra, in basso a
  sinistra; `--support-zone` nel CSS, z-index ≥ 1000). Il widget dovrà
  scegliere l'angolo leggendo `data-sidebar` su `<html>`. Non mettere nulla
  di fisso lì.
- **Homepage**: dall'alto il nome piccolo (`.home-name`, da `site.Title`),
  la promessa grande come **h1** (`.slogan`, una riga per parte: "Rendo il
  tuo" / NOME / "bello e desiderabile su internet."), i pulsanti (principale "Scopri
  cosa posso fare per te" → Servizi, secondario "Chiedimi un preventivo" →
  Contatti; chiavi i18n `home_cta` e `home_quote`) e sotto il paragrafo
  `description` (dopo i pulsanti, così si vedono senza scorrere). Testi in `slogan` di `languages.yaml` (`prefix`,
  `subjects`, `suffix`). Font dell'h1 con `clamp(28px, 9cqi, 48px)` (cqi =
  larghezza del contenuto) e `text-wrap: balance`: il nome più lungo
  (APPARTAMENTO) sta su una riga anche a 360 px di schermo; se aggiungi un
  nome più lungo, provalo lì. **Il primo nome di `subjects` è già scritto
  nell'HTML** (gli altri `.sp-subtitle` sono `display: none`): è quello che
  leggono Google e chi non ha JavaScript; con lo script attivo resta nascosto
  alla vista per gli screen reader. Effetto macchina da scrivere in
  `site.js` (blocco `[data-typewriter]`): scrive un nome una lettera alla
  volta con un cursore a blocco nel colore d'accento, pausa di 3 s con il
  cursore che lampeggia (0,5 s acceso / 0,5 s spento), cancella a velocità
  doppia e passa al successivo, in ciclo. Tempi nelle costanti `SCRITTURA`,
  `CANCELLAZIONE` (= metà della scrittura), `PAUSA`, `ATTESA`. La riga del
  nome ha `min-height` di una riga (il testo sotto non salta quando il nome è
  cancellato) e il cursore è in `position: absolute`, così non sposta la
  parola centrata. Con "Riduci movimento" attivo o senza JavaScript resta il
  primo nome, fermo.
- **Pagina Chi sono**: tutto il testo (bio, scheda, competenze, perché
  scegliere me, piani, esempi, pulsante) sta nel corpo di
  `content/about(.en).md`, compreso il titolo grande; `layouts/about.html` stampa solo `.Content` dentro
  `<div class="testo-blocchi">` (il `title` del front matter serve per il
  `<title>` e i meta). I titoli dei blocchi sono
  titoli markdown `### Parola <span>Evidenziata</span>` (il CSS di
  `.testo-blocchi h3` li fa uguali a `.block-title h3`). I blocchi grafici
  sono shortcode con parametri in `layouts/_shortcodes/`, ognuno con l'uso
  scritto in cima al file; quelli con contenuto accettano markdown e altri
  shortcode (es. `{{< dato "fares.discounted" >}}`):
  `riga` + `colonna 7|5|4` (colonne affiancate; oggi non usate nella
  pagina), `scheda lato=` + `voce titolo= nota=` (informazioni personali; con
  `lato="destra|sinistra"` la scheda va in `float` e il testo che la **segue**
  le scorre attorno, quindi si scrive prima del testo; sotto i 600px di
  contenuto sta sopra, a tutta larghezza; i titoli `###` hanno `clear: both`), `competenze` + `competenza nome= valore=` (barre),
  `conoscenze "a" "b"` (etichette), `timeline` + `tappa periodo= luogo= titolo=`
  (curriculum ed esempi di lavori), `certificati` + `certificato titolo= id=
  data= logo=` (logo in `assets/` o SVG in `static/`), `risposta titolo= immagine=` (immagine in
  `assets/images/answers/`), `piani` + `piano titolo= icona= prezzo= link=
  consigliato="true"` (contenuto: descrizione + elenco; le voci non incluse
  si barrano con `~~…~~`; il CSS mette il prezzo tra i due con `order`;
  `link` è facoltativo: senza, oggi il caso di tutti i piani, "Acquista" apre
  Contatti con `?oggetto=` = `buy_subject` di i18n, che `site.js` mette nel
  campo Oggetto),
  `pulsante pagina=|link=`. Gli esempi dei blocchi oggi non usati sono nei
  commenti del front matter di `about.md`. **Non mettere esempi di shortcode
  in commenti HTML** nel corpo: Hugo li eseguirebbe comunque.
  **Indentazione**: il contenuto degli shortcode si indenta di 4 spazi per
  livello (i tag del livello più esterno restano a inizio riga, altrimenti
  diventano codice). Funziona perché ogni shortcode toglie l'indentazione del
  suo contenuto con `_partials/rientro.html` (non `.InnerDeindent`, che conta
  anche la riga di spazi prima del tag di chiusura) e produce HTML su una riga
  sola con `_partials/compatta.html`, così annidato resta allineato. Uno
  shortcode nuovo deve fare lo stesso.
- **Testi con segnaposto**: in `languages.yaml` si
  possono scrivere `{{ params.fares.standard }}`, `{{ params.fares.discounted }}`
  e `{{ params.support.email }}`; li sostituisce `_partials/testo.html`.
- **Privacy**: il testo è il corpo HTML di `content/privacy(.en).md`; i dati
  (indirizzo, email, fornitori) stanno nel front matter e si richiamano con
  `{{< dato "chiave" >}}`; ogni servizio esterno usato dal sito (hosting,
  Umami, Formcarry, Turnstile, Google Fonts) ha la sua sezione: se ne aggiungi
  uno, aggiorna l'informativa e la data in tutte e due le lingue. Nei file markdown le righe HTML non vanno
  indentate (diventerebbero blocchi di codice).
- **Blog**: sezione Hugo normale, oggi vuota. I post (solo in italiano, mostrati
  anche in `/en/blog/`) saranno scritti in `content/blog/` dal progetto
  *memos 2 hugo* (markdown + front matter: `title`, `date`, `tags`,
  `image` = file del bundle o URL, che Hugo scarica e converte). Il comando andrà tra i `pre` di `build.toml`.
- **Feed RSS**: `/blog/index.xml` (`layouts/blog/section.rss.xml`), ultimi 20
  post con il corpo in HTML; attivato con `outputs: [html, rss]` solo nel
  `_index.md` italiano del blog. RSS disattivato altrove.
- **Form contatti**: backend **Formcarry** + Cloudflare **Turnstile** (script
  caricato solo in `contact.html`), indirizzi in `params.yaml`. Submit nativo,
  nessun JavaScript di invio. I campi usano `placeholder` per l'etichetta in CSS.
- **Ambiente di sviluppo**: `hugo server` usa l'ambiente "development" e legge
  anche `config/development/params.yaml`, che imposta la sitekey di prova di
  Turnstile (`1x00000000000000000000AA`, nessun errore su localhost) e
  `contact-form.simulate: true`: il form non ha l'action di Formcarry, mostra
  un avviso e l'invio viene intercettato da uno script (la validazione dei
  campi resta). `hugo` e `build.py` usano "production" e ignorano quella
  cartella. Per provare la configurazione vera in locale:
  `hugo server --environment production`.
- **404**: `layouts/404.html` genera `/404.html` (e `/en/404.html`).
- **i18n**: `it.json` ed `en.json` devono avere le stesse chiavi, senza
  duplicati. Le stringhe con `<span>` (parola evidenziata nei titoli) vanno
  stampate con `| safeHTML`.
- `return` nei partial deve essere l'ultimo comando: con una pipeline va tra
  parentesi (`{{ return (a | default b) }}`).

## SEO

- `head.html` genera meta description, Open Graph, canonical, `hreflang` e
  JSON-LD su ogni pagina. Descrizione: `description` nel front matter (c'è
  in Chi sono, contatti, privacy e negli `_index.md` delle sezioni); per le
  voci delle collezioni e i post il loro testo, accorciato a 160 caratteri;
  altrimenti la `description` del sito in `languages.yaml`. Dati strutturati: schema.org `Person`, costruito come dict e
  serializzato con `jsonify`, con `@id` fisso `<baseURL>#person`.
  `knowsAbout` dai `meta` dei servizi + `other` di
  `content/services/_index(.en).md`; `knowsLanguage` e `availableLanguage`
  dalle lingue del sito (`hugo.Sites`; `site.Languages` è deprecato da Hugo
  0.156). **Nessun testo scritto nel template**: `author.job`,
  `author.bio` (descrizione in terza persona) e `support.type/note/area`
  (il `contactPoint`) sono tradotti in `languages.yaml`; gli altri dati
  vengono da `params.yaml`. Le pagine con `schema: ProfilePage` nel front
  matter (`about(.en).md`) pubblicano un `ProfilePage` con la `Person` come
  `mainEntity`. Proprietà ammesse da schema.org per `Person`: niente
  `areaServed`/`availableLanguage` (stanno nel `ContactPoint`). I testi sono
  provvisori, come il resto del sito.
- Sitemap: `/sitemap.xml` è **un'unica sitemap con le pagine di tutte le
  lingue** (`layouts/sitemapindex.xml`, con alternates hreflang), non l'indice
  standard di Hugo: quello rimanderebbe a `/it/sitemap.xml`, che per il
  protocollo non può elencare le pagine italiane (stanno alla radice, fuori
  da `/it/`). Hugo pubblica comunque `/it/` e `/en/sitemap.xml` (non si
  possono spegnere da sole): Caddy li redirige a `/sitemap.xml`.
  changefreq/priority dal front matter `sitemap` (con `cascade` nelle sezioni).
  `lastmod` (anche `dateModified` nel JSON-LD): `lastmod` del front matter,
  poi l'ultimo commit git del file (`enableGitInfo`), poi la data del file;
  mai `date`, che è la data di pubblicazione.
- `robots.txt` da `layouts/robots.txt`.
- **llms.txt** (formato https://llmstxt.org): presentazione e domande
  frequenti per le IA, in `/llms.txt` e `/en/llms.txt` (formato `llms` in
  `hugo.yaml`, attivato negli `outputs` di `content/_index(.en).md`). Il
  testo (titolo, riassunto, FAQ in terza persona) sta in
  `content/llms/index(.en).md`, page bundle con
  `build: {render: never, list: never}`: niente pagina HTML, niente sitemap,
  non compare negli elenchi. Nel testo si usano `{{< dato "…" >}}` e
  `{{< ref "/pagina" >}}` (URL assoluti). `layouts/home.llms.txt` lo stampa
  con `.RenderShortcodes | htmlUnescape` e aggiunge in fondo, generati, le
  pagine del menu con le voci delle sezioni, i profili di `social` e il link
  all'altra lingua (titoli da i18n: `llms_pages`, `llms_profiles`,
  `llms_languages`). **Niente prezzi in llms.txt** (scelta di Francesco): per
  i costi si rimanda al preventivo gratuito.
- Favicon: l'avatar `static/favicon.png` (192×192), da cui sono ricavati
  `static/favicon.ico` (16/32/48 px) e `static/apple-touch-icon.png` (180 px);
  i link sono in `head.html`. Se cambi l'avatar della favicon, rigenera anche
  gli altri due file. `static/images/logo.svg` (la scritta "C | FRANCESCO
  MAIDA", bianca e larga) non è adatto come favicon.

## Caddy (VPS)

Il server web è **Caddy**, che non legge file per cartella come `.htaccess`.
Le regole del sito stanno in `layouts/home.caddy`, che Hugo pubblica come
`/.caddy` nella radice della cartella di deploy; il Caddyfile del server le
include una volta sola con `import <cartella del sito>/.caddy` dentro il
blocco del sito (dopo ogni modifica: `caddy reload`).

**File senza estensione generati dalla home.** `content/_index.md` (solo
quello italiano) ha `outputs: [html, webfinger, atproto-did, caddy]`; i
formati sono in `hugo.yaml` (`mediaTypes` con suffisso vuoto = nessuna
estensione, `outputFormats` con `path: .well-known` per i primi due) e i
template sono `layouts/home.<formato>`. I dati stanno in `params.yaml`
(`fediverse`, `bluesky`): per cambiarli non si toccano i template.

Il file `.caddy` contiene:
- il blocco dell'accesso a `/.caddy` stesso (404; con `hugo server` invece
  si legge);
- **WebFinger** per Mastodon: `GET /.well-known/webfinger?resource=acct:<fediverse.alias>`
  risponde con il JSON di `home.webfinger` (`subject` = l'account Mastodon
  vero, `acct:<user>@<server>`, perché Mastodon lo riverifica lì; più profilo,
  attore ActivityPub e modello di "segui"), con `Content-Type:
  application/jrd+json` e `Access-Control-Allow-Origin: *`; altri `resource`
  o nessuno → 404, metodi diversi da GET/HEAD → 405 (`file_server`);
- **Bluesky**: `/.well-known/atproto-did` (da `home.atproto-did`) contiene
  `bluesky.did`, senza a capo finale, servito come `text/plain`; serve per
  usare il dominio come handle. Bluesky non usa WebFinger: l'handle è il
  dominio (`@cesco.it`), non un indirizzo come quello di Mastodon;
- i redirect 301 dal vecchio sito Flask: `/rss/` → `/blog/index.xml` e
  `/static/…` → `/…` (i file statici non hanno più il prefisso);
- i **codici QR corti**: `https://cesco.it/<codice>` (anche con `/`
  finale) rimanda alla destinazione con un **302**. **Formato: 4 caratteri
  tra A-Z e 2-9, maiuscole e minuscole indifferenti**: niente `0` e `1`, che
  ricopiando dalla carta si confondono con `O` e `I`/`L`; 34⁴ = 1.336.336
  combinazioni. `/ab23`, `/AB23` e `/Ab23` sono lo stesso codice, e in
  `params.yaml` si può scrivere in qualsiasi modo. Funziona perché il
  matcher `path` di Caddy non distingue maiuscole e minuscole e Hugo mette in
  minuscolo i nomi dei params; i controlli del template (pagine, file di
  `static/`) confrontano tutto in minuscolo. I codici sono pochi e si creano
  a mano, uno alla volta. Non è un 301 perché la destinazione deve poter
  cambiare: i QR stampati non si ritirano. I codici stanno nella mappa `qr`
  di `params.yaml` (`codice: destinazione`, URL assoluto o percorso che
  inizia con `/`; oggi vuota). Ogni voce genera `@qr_<codice> path …` +
  `redir … temporary`. La build si ferma se il codice non rispetta il
  formato, se la destinazione non è valida o se il codice coincide con una
  pagina (di qualsiasi lingua) o con un file di `static/`. Sono solo regole di Caddy: niente pagine Hugo, quindi
  non compaiono nella sitemap. **Un codice non si riassegna mai** a un'altra
  cosa: se non serve più, lo si fa puntare a una pagina utile. Dopo ogni
  modifica: deploy + `caddy reload`.
  Servono per codici QR piccoli e robusti da stampare (es. la brochure di un
  servizio). **Nel QR si scrive l'URL tutto maiuscolo e senza `/` finale**
  (`HTTPS://CESCO.IT/ABCD`): così il QR usa la modalità alfanumerica
  (5,5 bit per carattere invece di 8) e a parità di dimensione regge più
  danni. A 25×25 moduli ha la correzione Q (~25%) invece della M (~15%) del
  minuscolo, che con la Q sale a 29×29. Per misurare le scansioni in
  Umami, la destinazione può avere i parametri UTM
  (`/servizi/…/?utm_source=brochure&utm_medium=qr`);
- `handle_errors 404` con `/404.html` (e `/en/404.html` sotto `/en/`),
  che richiede Caddy ≥ 2.8.

## Repository

- GitHub: `fmaida/cesco.it` (pubblico), branch `main`. La cronologia è
  ripartita da zero il 2026-10-03 con il passaggio a Hugo (push forzato).
  I commit del vecchio sito Flask restano su GitHub solo come commit
  orfani (ultimo: `6feaaf9`) finché non vengono agganciati a un branch.
- Nessun deploy automatico: niente `.github/workflows`, niente webhook. Su
  GitHub è ancora abilitato Pages (dominio `cesco.it`, sorgente "workflow")
  e potrebbe esistere un vecchio sito Netlify: sono residui, il sito è
  pubblicato solo sul VPS.
- Mai `git push --force` senza conferma esplicita di Francesco.

## Test

Il progetto non ha una suite di test. Verifica: `hugo -d <cartella
temporanea>` senza errori né warning (non `hugo` da solo, che scrive nella
cartella di deploy), poi `hugo server` e controllo delle pagine nelle due lingue.

## Metadata
- Ultima modifica: 2026-10-06
- Modello: claude-opus-5-5
