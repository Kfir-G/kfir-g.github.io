import frontmatter
import os
from datetime import datetime

docs_path = "docs/podcasts"
rss_items = []

for file in os.listdir(docs_path):
    if file.endswith(".md"):
        post = frontmatter.load(os.path.join(docs_path, file))
        title = post.get("title", "No Title")
        date = post.get("date", datetime.now().isoformat())
        audio = post.get("audio", "")
        rss_items.append(f"<item><title>{title}</title><enclosure url='{audio}' type='audio/mpeg'/><pubDate>{date}</pubDate></item>")

rss_feed = f"""<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>Kfir G Podcasts</title>
<link>https://kfir-g.github.io/podcasts</link>
{''.join(rss_items)}
</channel>
</rss>
"""

with open("site/podcasts/rss.xml", "w") as f:
    f.write(rss_feed)
print("Podcast RSS generated.")
