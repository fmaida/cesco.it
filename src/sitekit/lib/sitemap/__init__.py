from datetime import datetime
from urllib.parse import urljoin
from xml.sax.saxutils import escape
from sitekit.settings import BUILD_DIR, BASE_URL


url_list = []

def add(url: str, change_freq: str = "monthly", priority: float = None):
    global url_list

    if priority is None:
        homepage_variants = {"", "/", "index.html", "/index.html"}
        priority = 1.0 if url in homepage_variants else 0.5

    abs_path = urljoin(BASE_URL + "/", url)
    url_list.append((abs_path, change_freq, priority))

def generate():
    today = datetime.now().strftime("%Y-%m-%d")

    with open(BUILD_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")
        for url in url_list:
            f.write(f"  <url>\n")
            f.write(f"    <loc>{escape(url[0])}</loc>\n")
            f.write(f"    <lastmod>{today}</lastmod>\n")
            f.write(f"    <changefreq>{url[1]}</changefreq>\n")
            f.write(f"    <priority>{url[2]}</priority>\n")
            f.write(f"  </url>\n")
        f.write("</urlset>\n")