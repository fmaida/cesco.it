import re
import sys
import warnings
from pathlib import Path

# Fix automatico del PYTHONPATH per GitHub Actions
current_dir = Path(__file__).parent.parent  # va in src/
sys.path.insert(0, str(current_dir))

from sitekit import content, i18n, cache, images, pagebundle, sitemap, robots
from sitekit.settings import settings
from flask_frozen import Freezer, NotFoundWarning
from flask_minify import Minify
from main.app import app

# Copio i file direttamente qua
settings.BUILD_DIR = Path.home() / "Sites" / "cesco.it"

# Assicura che, in assenza di estensioni, il contenuto HTML venga gestito correttamente
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
# (Facoltativo) evita warning sui mimetype durante il freeze
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_DESTINATION'] = str(settings.BUILD_DIR)
app.config['FREEZER_BASE_URL'] = settings.BASE_URL
# La pagina 404 ora risponde (correttamente) con status 404:
# senza questa opzione Frozen-Flask interromperebbe il freeze.
# Con l'opzione attiva la pagina viene comunque generata.
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True

# Il generatore error_handlers() qua sotto visita apposta un URL
# inesistente per forzare la creazione di 404.html: il warning che ne
# consegue è quindi previsto e va silenziato solo per quell'URL preciso,
# senza nascondere un NotFoundWarning su un URL diverso (segnalerebbe
# un problema reale, come il bug sulle immagini responsive già risolto).
warnings.filterwarnings(
    "ignore",
    category=NotFoundWarning,
    message=re.escape("Ignored '404 NOT FOUND' on URL /404.html"),
)

Minify(app=app, html=True, js=False, cssless=False)

freezer = Freezer(app, log_url_for=True)


@freezer.register_generator
def error_handlers():
    # Questa pagina non esiste appositamente
    # per triggerare la creazione della pagina 404
    yield "/404.html"


@freezer.register_generator
def privacy():
    yield 'privacy', {}  # per /privacy senza parametri


def pregenerazione_immagini():
    """
    Pre-genera tutte le immagini prima del freeze.
    """

    print("🖼️Pre-generazione immagini...")

    # Carica la configurazione
    temp = content.load("_config.yaml")
    temp["projects"] = content.load("projects", "_config.yaml")
    temp["answers"] = content.load("answers", "_config.yaml")

    # Pre-genera immagini answers
    for answer in temp["answers"]["answers"]:
        source_image = answer.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = settings.CONTENT_DIR / "answers" / source_image
            if source_image.exists():
                images.copy(source_image=source_image,
                            destination_folder=settings.STATIC_DIR / "cache" / "answers",
                            aspect_ratio="16:10")

    # Pre-genera immagini progetti
    for project in temp["projects"]["projects"]:
        source_image = project.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = settings.CONTENT_DIR / "projects" / source_image
            if source_image.exists():
                aspect_ratio = "1:1"
                anchor = "middle"
                if "siti_web" in project["tags"]:
                    aspect_ratio = "1:2"
                    anchor = "top"
                elif "documenti" in project["tags"]:
                    aspect_ratio = "2:3"
                elif "app" in project["tags"]:
                    aspect_ratio = "16:9"
                images.copy(source_image=source_image,
                            destination_folder=settings.STATIC_DIR / "cache" / "projects",
                            aspect_ratio=aspect_ratio, anchor=anchor)

    posts = pagebundle.load_collection(settings.CONTENT_DIR / "blog")

    print("✅ Pre-generazione immagini completata")


def main():

    # PRE-GENERA LE IMMAGINI PRIMA DEL FREEZE
    pregenerazione_immagini()

    # Inizia il processo di freeze
    try:
        freezer.freeze()
        sitemap.add(url="/", change_freq="monthly", priority=1)
        sitemap.add(url="/privacy/", change_freq="yearly", priority=0.2)
        sitemap.generate()
        print("✅ Sitemap creata con successo")
        print("✅ Freeze completato")
    except Exception as e:
        # Una build rotta deve fallire in modo visibile:
        # niente pulizia cache, exit code diverso da zero.
        print("❌ Errore durante freeze:", e)
        sys.exit(1)

    # Pulisce la cache da
    # eventuali file cache non
    # più utilizzati
    cache.clean()
    images.imgcache.clean()

    # Crea robots.txt ottimizzato per l'indicizzazione
    robots.generate()


if __name__ == '__main__':
    main()
