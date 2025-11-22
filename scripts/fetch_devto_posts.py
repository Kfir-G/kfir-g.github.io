import requests
import os

USERNAME = "kfir-g"
OUTPUT_DIR = "docs/blog"
os.makedirs(OUTPUT_DIR, exist_ok=True)

page = 1
while True:
    url = f"https://dev.to/api/articles?username={USERNAME}&page={page}&per_page=100"
    resp = requests.get(url)
    posts = resp.json()
    
    if not posts:
        break  # no more posts

    for post in posts:
        date = post["published_at"][:10]  # YYYY-MM-DD
        title = post["title"].replace("/", "-").replace(" ", "-")
        filename = f"{date}-{title}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        content = f"---\ntitle: {post['title']}\ndate: {date}\noriginal_url: {post['url']}\n---\n\n{post['body_markdown']}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Saved {filename}")

    page += 1
