import frontmatter
import requests
import os

DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")
MEDIUM_TOKEN = os.environ.get("MEDIUM_TOKEN")
MEDIUM_USER_ID = os.environ.get("MEDIUM_USER_ID")

# Example: iterate blog posts
for file in os.listdir("docs/blog/blogs"):
    if file.endswith(".md"):
        post = frontmatter.load(f"docs/blog/blogs/{file}")
        title = post.get("title", "Untitled")
        content = post.content

        # TODO: Post to Dev.to
        # TODO: Post to Medium
        print(f"Would publish: {title}")
