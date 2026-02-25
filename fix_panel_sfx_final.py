import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

content = content.replace("showReload() {\n        this.scene.audioManager.ui_click.play();", "showReload() {")
content = content.replace("hideReload() {\n        this.scene.audioManager.ui_click.play();", "hideReload() {")

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)
