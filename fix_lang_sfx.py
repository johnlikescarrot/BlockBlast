import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

content = content.replace("this.scene.i18n.setLanguage(lang);\n                this.scene.scene.restart();",
                         "this.scene.i18n.setLanguage(lang);\n                this.scene.audioManager.ui_click.play();\n                this.scene.scene.restart();")

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)
