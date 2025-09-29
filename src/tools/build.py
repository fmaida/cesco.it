import sys
from pathlib import Path

# Fix automatico del PYTHONPATH per GitHub Actions
current_dir = Path(__file__).parent.parent  # va in src/
sys.path.insert(0, str(current_dir))

from sitekit.settings import BUILD_DIR
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

def main():        
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
