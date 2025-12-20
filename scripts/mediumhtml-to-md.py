#!/usr/bin/env python3
import html2text
from pathlib import Path
from datetime import datetime
import re

# Change this to your Medium export posts folder
POSTS_DIR = Path("scripts/posts").expanduser()
OUTPUT_DIR = Path("docs/blog/old-blogs").expanduser()
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Default tags if you want
DEFAULT_TAGS = ["medium", "blog", "python"]

def html_to_md(html_file: Path) -> str:
    with html_file.open("r", encoding="utf-8") as f:
        html = f.read()
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    return h.handle(html)

def get_title_from_filename(filename: str) -> str:
    # Remove date prefix and id hash, replace '-' with space
    name = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", filename)
    name = re.sub(r"-[0-9a-f]{8,}\.html$", "", name)
    name = name.replace("-", " ")
    return name.strip().title()

for html_file in POSTS_DIR.glob("*.html"):
    md_content = html_to_md(html_file)
    
    # Extract date from filename
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", html_file.name)
    if date_match:
        date_str = date_match.group(1) + " 03:28:33 UTC"  # default time
    else:
        date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    title = get_title_from_filename(html_file.name)
    canonical_url = f"https://medium.com/p/{html_file.stem[-12:]}"  # fallback, adjust if needed

    frontmatter = f"""---
title: {title}
published: true
date: {date_str}
tags: {','.join(DEFAULT_TAGS)}
canonical_url: {canonical_url}
---
"""

    output_file = OUTPUT_DIR / (html_file.stem + ".md")
    with output_file.open("w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + md_content)

    print(f"Converted {html_file.name} → {output_file.name}")
