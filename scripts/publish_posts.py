import os, json, glob, frontmatter
import requests

DEVTO_TOKEN = os.getenv("DEVTO_TOKEN")
MEDIUM_TOKEN = os.getenv("MEDIUM_TOKEN")

published_file = ".published.json"
if os.path.exists(published_file):
    published = json.load(open(published_file))
else:
    published = {}

for md_file in glob.glob("docs/blog/*.md"):
    post = frontmatter.load(md_file)
    slug = os.path.basename(md_file)
    if slug in published:
        continue
    # Send to Dev.to
    if "devto" in post.get("publish_to", []):
        requests.post("https://dev.to/api/articles",
            headers={"api-key": DEVTO_TOKEN},
            json={"article":{"title":post["title"],"body_markdown":post.content,"published":True}})
    # Send to Medium
    if "medium" in post.get("publish_to", []):
        requests.post(f"https://api.medium.com/v1/users/{os.getenv('MEDIUM_USER_ID')}/posts",
            headers={"Authorization": f"Bearer {MEDIUM_TOKEN}"},
            json={"title":post["title"],"contentFormat":"markdown","content":post.content,"publishStatus":"public"})
    published[slug] = True

with open(published_file,"w") as f:
    json.dump(published,f,indent=2)
