import sys
from pathlib import Path

# Fix automatico del PYTHONPATH per GitHub Actions
current_dir = Path(__file__).parent.parent  # va in src/
sys.path.insert(0, str(current_dir))

from sitekit.settings import BUILD_DIR, CONTENT_DIR, STATIC_DIR
from tools.misc import create_robots_txt
from flask_frozen import Freezer
from main.app import app
from sitekit.lib import cache, images

# Assicura che, in assenza di estensioni, il contenuto HTML venga gestito correttamente
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
# (Facoltativo) evita warning sui mimetype durante il freeze
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_DESTINATION'] = str(BUILD_DIR)
# (rimosso FREEZER_IGNORE_ENDPOINTS: non supportato da frozen-flask)

# Assicura che Flask-Frozen costruisca URL con prefisso '/'
app.config.setdefault('FREEZER_BASE_URL', '/')

freezer = Freezer(app, log_url_for=True)


@freezer.register_generator
def error_handlers():
    # Questa pagina non esiste appositamente
    # per triggerare la creazione della pagina 404
    yield "/404.html"


@freezer.register_generator
def privacy():
    yield 'privacy', {}  # per /privacy senza parametri


def pregenerazioneImmagini():
    """Pre-genera tutte le immagini prima del freeze"""
    print("🖼️  Pre-generazione immagini...")

    # Carica la configurazione
    temp = cache.load(CONTENT_DIR / "_config.yaml")
    temp["projects"] = cache.load(CONTENT_DIR / "projects" / "_config.yaml")
    temp["answers"] = cache.load(CONTENT_DIR / "answers" / "_config.yaml")

    # Pre-genera immagini answers
    for answer in temp["answers"]["answers"]:
        source_image = answer.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = CONTENT_DIR / "answers" / source_image
            if source_image.exists():
                images.copy(source_image=source_image,
                            destination_folder=STATIC_DIR / "cache" / "answers",
                            aspect_ratio="16:10")

    # Pre-genera immagini progetti
    for project in temp["projects"]["projects"]:
        source_image = project.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = CONTENT_DIR / "projects" / source_image
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
                            destination_folder=STATIC_DIR / "cache" / "projects",
                            aspect_ratio=aspect_ratio, anchor=anchor)

    print("✅ Pre-generazione immagini completata")


def main():
    # PRE-GENERA LE IMMAGINI PRIMA DEL FREEZE
    pregenerazioneImmagini()

    # Inizia il processo di freeze
    print("Endpoint registrati:", sorted(app.view_functions.keys()))
    try:
        freezer.freeze()
        print("✅ Freeze completato")
    except Exception as e:
        print("❌ Errore durante freeze:", e)

    # Pulisce la cache da 
    # eventuali file cache non
    # più utilizzati
    cache.clean()
    images.imgcache.salva()

    # Crea robots.txt ottimizzato per l'indicizzazione
    create_robots_txt()


if __name__ == '__main__':
    main()