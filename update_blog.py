import html
import re
import urllib.request

import feedparser

# Each feed fills its own marker section in README.md.
# To retire Tistory later, delete its line here and its block in README.md.
FEEDS = [
    ("BLOG-POST-LIST", "https://chanhi.github.io/rss.xml"),
    ("TISTORY-POST-LIST", "https://chanhuy.tistory.com/rss"),
]
MAX_POSTS = 5
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}


def fetch_posts(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        feed = feedparser.parse(response.read())
    lines = []
    for entry in feed.entries[:MAX_POSTS]:
        title = html.unescape(entry.title)  # turns "&amp;" into "&"
        lines.append(f"- [{title}]({entry.link})")
    return "\n".join(lines) + "\n" if lines else ""


with open("README.md", "r", encoding="utf-8") as f:
    readme_text = f.read()

for marker, url in FEEDS:
    try:
        posts = fetch_posts(url)
    except Exception as e:
        # If one feed fails, keep its previous list and still update the others.
        print(f"[skip] {marker}: {e}")
        continue
    if not posts:
        print(f"[skip] {marker}: no entries")
        continue
    readme_text = re.sub(
        rf"<!-- {marker}:START -->.*?<!-- {marker}:END -->",
        lambda _: f"<!-- {marker}:START -->\n{posts}<!-- {marker}:END -->",
        readme_text,
        flags=re.DOTALL,
    )

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_text)
