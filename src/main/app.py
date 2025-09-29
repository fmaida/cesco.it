from flask import Flask, request, redirect
from flask import render_template
from markdown import markdown
from markupsafe import Markup
from sitekit.settings import (BASE_DIR,
                              CONTENT_DIR,
                              I18N_DIR,
                              TEMPLATES_DIR, 
                              STATIC_DIR)
from sitekit.lib import cache
from sitekit.lib import images
from sitekit.lib import pagebundle
from datetime import datetime
import time


app = Flask(__name__, 
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)


@app.template_filter("markdown")
def markdown_filter(text):
    return Markup(markdown(text, extensions=["extra", "tables"]))

@app.route("/", endpoint='home')
def home():
    start = time.perf_counter()  # punto A
    temp = cache.load(CONTENT_DIR / "_config.yaml")
    app.config["SERVER_NAME"] = temp["base-url"]
    temp["projects"] = cache.load(CONTENT_DIR / "projects" / "_config.yaml")
    temp["services"] = cache.load(CONTENT_DIR / "services" / "_config.yaml")
    temp["examples"] = cache.load(CONTENT_DIR / "examples" / "_config.yaml")
    temp["plans"] = cache.load(CONTENT_DIR / "plans" / "_config.yaml")
    temp["answers"] = cache.load(CONTENT_DIR / "answers" / "_config.yaml")
    for index, answer in enumerate(temp["answers"]["answers"]):
        source_image = answer.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = CONTENT_DIR / "answers" / source_image
            images.copy(source_image=source_image,
                        destination_folder=STATIC_DIR / "cache" / "answers", aspect_ratio="16:10")
            answer["image_path"] = "cache/answers/" + source_image.stem + "/" + source_image.stem
            answer["aspect_ratio"] = "16:10"
    for index, project in enumerate(temp["projects"]["projects"]):
        source_image = project.get("image")
        if source_image and not source_image.startswith("/"):
            source_image = CONTENT_DIR / "projects" / source_image
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
            project["image_path"] = "cache/projects/" + source_image.stem + "/" + source_image.stem
            project["aspect_ratio"] = aspect_ratio
            #temp["projects"]["projects"][index]["image"] = "cache/projects/" + source_image.stem + "/" + source_image.stem
    t = cache.load(I18N_DIR / "it.json")
    pagebundle.set_media_destination_folder(STATIC_DIR / "cache" / "blog")
    posts = pagebundle.load_collection(CONTENT_DIR / "blog")
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
                           posts=posts[:3],
                           now=datetime.now())

@app.route("/privacy", endpoint='privacy')
def privacy_policy():
    temp = cache.load(CONTENT_DIR / "_config.yaml")
    temp["privacy"] = cache.load(CONTENT_DIR / "privacy" / "_config.yaml")
    t = cache.load(I18N_DIR / "it.json")
    return render_template('privacy.html',
                           params=temp,
                           t=t,
                           now=datetime.now())

@app.errorhandler(404)
def page_not_found(e):
    t = cache.load(I18N_DIR / "it.json")
    return render_template("404.html",
                           t=t,
                           params={"description": "Pagina non trovata"})