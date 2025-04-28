An AI mental health assistant
import os

readme_path = "README.md"
screenshots_dir = "Screenshots"

markdown = "\n## Screenshots\n"
for file in os.listdir(screenshots_dir):
    if file.endswith((".png", ".jpg", ".jpeg")):
        markdown += f"![{file}](./{screenshots_dir}/{file})\n"

with open(readme_path, "a") as f:
    f.write(markdown)
