from datetime import datetime
from pathlib import Path

import grabmymemos
from flask import Flask, render_template
from markdown import markdown
from markupsafe import Markup
from sitekit import content, i18n, images
from sitekit.settings import settings


app = Flask(__name__,
            template_folder=settings.TEMPLATES_DIR,
            static_folder=settings.STATIC_DIR)

# Imposta il sito base
settings.BASE_URL = "https://cesco.it"

# Prefisso URL dei file statici, per costruire a mano i percorsi delle
# immagini responsive senza passare da url_for() su un file "base" che
# non esiste mai di per sé (esistono solo le varianti __400.jpg ecc.):
# altrimenti Frozen-Flask lo scopre come URL da congelare, lo trova 404
# e ne scrive la pagina d'errore come file dentro la cartella immagini.
app.jinja_env.globals["STATIC_URL"] = app.static_url_path


@app.template_filter("markdown")
def markdown_filter(text: str) -> Markup:
    return Markup(markdown(text, extensions=["extra", "tables"]))


def _carica_posts() -> list:
    """
    Scarica da Memos gli ultimi post taggati #lavoro.

    Se il server Memos non è raggiungibile (o il token manca),
    restituisce una lista vuota invece di far fallire la build:
    la sezione blog mostrerà il messaggio "nessun articolo".

    Returns:
        list: I post scaricati, oppure una lista vuota.
    """

    token = Path.home() / ".config" / "cesco.it" / "memos.token"
    try:
        grabmymemos.config(base_url="https://memos.cesco.it", token=token)
        grabmymemos.always_force_a_title()
        grabmymemos.wrap_titles_at(length=30)

        return grabmymemos.fetch(tags=["lavoro"])
    except Exception as errore:
        print(f"⚠️ Impossibile scaricare i post da Memos: {errore}")

        return []


@app.route("/", endpoint="home")
def home() -> str:
    temp = content.load("_config.yaml")
    temp["projects"] = content.load("projects", "_config.yaml")
    temp["services"] = content.load("services", "_config.yaml")
    temp["examples"] = content.load("examples", "_config.yaml")
    temp["plans"] = content.load("plans", "_config.yaml")
    temp["answers"] = content.load("answers", "_config.yaml")

    # Immagini nelle risposte ("perché scegliere me")
    for answer in temp["answers"]["answers"]:
        source_image = answer.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = settings.CONTENT_DIR / "answers" / source_image
            images.copy(source_image=source_image,
                        destination_folder=settings.STATIC_DIR / "cache" / "answers",
                        aspect_ratio="16:10")
            answer["image_path"] = "cache/answers/" + source_image.stem + "/" + source_image.stem
            answer["aspect_ratio"] = "16:10"

    # Immagini nei progetti
    for project in temp["projects"]["projects"]:
        source_image = project.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = settings.CONTENT_DIR / "projects" / source_image
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
            project["image_path"] = "cache/projects/" + source_image.stem + "/" + source_image.stem
            project["aspect_ratio"] = aspect_ratio

    t = i18n.load("it.json")

    # Scarica da Memos gli ultimi post taggati #lavoro
    posts = _carica_posts()

    return render_template('index.html',
                           params=temp,
                           t=t,
                           posts=posts,
                           now=datetime.now())


@app.route("/privacy/", endpoint="privacy")
def privacy_policy() -> str:
    temp = content.load("_config.yaml")
    temp["privacy"] = content.load("privacy", "_config.yaml")
    t = i18n.load("it.json")

    return render_template('privacy.html',
                           params=temp,
                           t=t,
                           now=datetime.now())


@app.errorhandler(404)
def page_not_found(e) -> tuple:
    temp = content.load("_config.yaml")
    t = i18n.load("it.json")

    return render_template("404.html",
                           params=temp,
                           t=t,
                           now=datetime.now()), 404
