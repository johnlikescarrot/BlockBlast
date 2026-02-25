import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

# Pause panel: optionsButton
content = content.replace("optionsButton.on('pointerdown', () => {\n            this.hidePause();",
                         "optionsButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hidePause();")

# Pause panel: exitButton
content = content.replace("exitButton.on('pointerdown', () => {\n            this.hidePause();",
                         "exitButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hidePause();")

# Reload panel: reloadButton
content = content.replace("reloadButton.on('pointerdown', () => {\n            this.hideReload();",
                         "reloadButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hideReload();")

# Score panel: restartButton
content = content.replace("restartButton.on('pointerdown', () => {\n            this.hideScore();",
                         "restartButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hideScore();")

# Score panel: menuButton
content = content.replace("menuButton.on('pointerdown', () => {\n            this.hideScore();",
                         "menuButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hideScore();")

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)
