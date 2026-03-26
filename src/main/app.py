from flask import Flask, request, redirect
from flask import render_template
from markdown import markdown
from markupsafe import Markup
from sitekit import content, i18n, images, memos
from sitekit.settings import settings
from datetime import datetime
from pathlib import Path
import time


app = Flask(__name__, 
            template_folder=settings.TEMPLATES_DIR,
            static_folder=settings.STATIC_DIR)

# Imposta il sito base
settings.BASE_URL = "https://cesco.it"


@app.template_filter("markdown")
def markdown_filter(text):
    return Markup(markdown(text, extensions=["extra", "tables"]))

@app.route("/", endpoint='home')
def home():
    start = time.perf_counter()  # punto A
    temp = content.load("_config.yaml")
    app.config["SERVER_NAME"] = temp["base-url"]
    temp["projects"] = content.load("projects", "_config.yaml")
    temp["services"] = content.load("services", "_config.yaml")
    temp["examples"] = content.load("examples", "_config.yaml")
    temp["plans"] = content.load("plans", "_config.yaml")
    temp["answers"] = content.load("answers", "_config.yaml")
    for index, answer in enumerate(temp["answers"]["answers"]):
        source_image = answer.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = settings.CONTENT_DIR / "answers" / source_image
            images.copy(source_image=source_image,
                        destination_folder=settings.STATIC_DIR / "cache" / "answers", aspect_ratio="16:10")
            answer["image_path"] = "cache/answers/" + source_image.stem + "/" + source_image.stem
            answer["aspect_ratio"] = "16:10"

    # Immagini nei progetti
    for index, project in enumerate(temp["projects"]["projects"]):
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
            #temp["projects"]["projects"][index]["image"] = "cache/projects/" + source_image.stem + "/" + source_image.stem
    t = i18n.load("it.json")


    token = Path.home() / ".config" / "cesco.it" / "memos.token"
    memos.set_token(token)
    memos.set_base_url("https://memos.cesco.it")
    #memos.set_base_url("https://cesco.blog")
    memos.set_force_a_title(True)
    memos.set_wrap_titles_at(30)
    posts = memos.get()

    #pagebundle.set_media_destination_folder(settings.STATIC_DIR / "cache" / "blog")
    #posts = pagebundle.load_collection(settings.CONTENT_DIR / "blog")

    #print(a)
    #print(b)
    # source = CONTENT_DIR / "blog" / "post-1" / "immagine_cover.jpg"
    # destination = STATIC_DIR / "images"
    # temp["image"] = images.copy(source, destination)
    end = time.perf_counter()
    temp["elapsed_time"] = end - start
    return render_template('index.html',
                           params=temp,
                           t=t,
                           posts=posts,
                           now=datetime.now())

@app.route("/privacy/", endpoint='privacy')
def privacy_policy():
    temp = content.load("_config.yaml")
    temp["privacy"] = content.load("privacy", "_config.yaml")
    t = i18n.load("it.json")
    return render_template('privacy.html',
                           params=temp,
                           t=t,
                           now=datetime.now())

@app.errorhandler(404)
def page_not_found(e):
    temp = content.load("_config.yaml")
    t = i18n.load("it.json")
    return render_template("404.html",
                           params=temp,
                           t=t,
                           now=datetime.now())