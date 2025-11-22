# fetch_medium_posts.py
import feedparser
import html2text
import os
from datetime import datetime

# RSS feed of your Medium account
RSS_FEED_URL = "https://medium.com/feed/@Kfir-G"

# Where to save Markdown files
OUTPUT_DIR = "docs/blog"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parse the RSS feed
feed = feedparser.parse(RSS_FEED_URL)

for entry in feed.entries:
    # Create a safe filename from the title
    title_safe = entry.title.replace("/", "-").replace(" ", "-")
    date_str = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
    filename = f"{date_str}-{title_safe}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Skip if this file already exists
    if os.path.exists(filepath):
        print(f"Already exists, skipping: {filename}")
        continue

    # Convert HTML content to Markdown
    html_content = entry.content[0].value if 'content' in entry else entry.summary
    md_content = html2text.html2text(html_content)

    # Add frontmatter for MkDocs
    frontmatter = f"---\ntitle: {entry.title}\ndate: {date_str}\noriginal_url: {entry.link}\n---\n\n"

    # Save the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + md_content)

    print(f"Saved: {filepath}")

print("Medium posts fetched and saved successfully!")
