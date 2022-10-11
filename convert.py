import markdown

with open('release.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text, extensions=['pymdownx.emoji'])

with open('release.html', 'w') as f:
    f.write(html)
