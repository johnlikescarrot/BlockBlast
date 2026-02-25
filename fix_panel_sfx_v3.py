import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

# Instructions panel close button
content = content.replace("closeImage.on('pointerdown', () => {\n            this.hideInstructions();",
                         "closeImage.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hideInstructions();")

# Ensure showPause/hidePause/showOptions/hideOptions don't have play() calls internally
# (We already did this but let's be sure)

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)
