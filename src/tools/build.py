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

freezer = Freezer(app)


@freezer.register_generator
def error_handlers():
    # Questa pagina non esiste appositamente
    # per triggerare la creazione della pagina 404
    yield "/404.html"

def main():        
    # Inizia il processo di freeze
    freezer.freeze()

    # Pulisce la cache da 
    # eventuali file cache non
    # più utilizzati
    cache.clean()
    images.imgcache.salva()

    # Crea robots.txt ottimizzato per l'indicizzazione
    create_robots_txt()

if __name__ == '__main__':
    main()
