import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

# Remove sounds from base methods
content = content.replace("showPause() {\n        this.scene.audioManager.ui_click.play();", "showPause() {")
content = content.replace("hidePause() {\n        this.scene.audioManager.ui_click.play();", "hidePause() {")
content = content.replace("showOptions() {\n        this.scene.audioManager.ui_click.play();", "showOptions() {")
content = content.replace("hideOptions() {\n        this.scene.audioManager.ui_click.play();", "hideOptions() {")
content = content.replace("showCredits() {\n        this.scene.audioManager.ui_click.play();", "showCredits() {")
content = content.replace("hideCredits() {\n        this.scene.audioManager.ui_click.play();", "hideCredits() {")
content = content.replace("hideInstructions() {\n        this.scene.audioManager.ui_click.play();", "hideInstructions() {")

# Add sounds to handlers where missing
content = content.replace("closeImage.on('pointerdown', () => { this.scene.audioManager.resumeMusic(); this.scene.currentScene.PauseGame(); });",
                         "closeImage.on('pointerdown', () => { this.scene.audioManager.ui_click.play(); this.scene.audioManager.resumeMusic(); this.scene.currentScene.PauseGame(); });")
content = content.replace("optionsButton.on('pointerdown', () => {\n            this.hidePause(); \n            this.showOptions();\n        });",
                         "optionsButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hidePause(); \n            this.showOptions();\n        });")
content = content.replace("exitButton.on('pointerdown', () => {\n            this.hidePause();\n            this.scene.currentScene.BackMenu();\n        });",
                         "exitButton.on('pointerdown', () => {\n            this.scene.audioManager.ui_click.play();\n            this.hidePause();\n            this.scene.currentScene.BackMenu();\n        });")
content = content.replace("closeImage.on('pointerdown', () => { this.scene.audioManager.resumeMusic(); this.scene.currentScene.ReloadGame(); });",
                         "closeImage.on('pointerdown', () => { this.scene.audioManager.ui_click.play(); this.scene.audioManager.resumeMusic(); this.scene.currentScene.ReloadGame(); });")
content = content.replace("closeImage.on('pointerdown', () => this.hideCredits());",
                         "closeImage.on('pointerdown', () => { this.scene.audioManager.ui_click.play(); this.hideCredits(); });")
content = content.replace("closeImage.on('pointerdown', () => this.hideOptions());",
                         "closeImage.on('pointerdown', () => { this.scene.audioManager.ui_click.play(); this.hideOptions(); });")

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)
