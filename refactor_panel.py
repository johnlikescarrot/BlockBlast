import sys

with open('src/scripts/components/panel.js', 'r') as f:
    content = f.read()

# 1. Fix hideInstructions callback timing
old_hide_instructions = """    hideInstructions() {
        this.animateHide(this.instructionsContainer, () => {
            this.panelContainer.setVisible(false);
        });
        if (this._hideInstructionsCallback) {
            const cb = this._hideInstructionsCallback;
            this._hideInstructionsCallback = null;
            cb();
        }
    }"""

new_hide_instructions = """    hideInstructions() {
        this.animateHide(this.instructionsContainer, () => {
            this.panelContainer.setVisible(false);
            if (this._hideInstructionsCallback) {
                const cb = this._hideInstructionsCallback;
                this._hideInstructionsCallback = null;
                cb();
            }
        });
    }"""

content = content.replace(old_hide_instructions, new_hide_instructions)

# 2. Fix hidePause to accept a callback
old_hide_pause = """    hidePause() {
        this.animateHide(this.pauseContainer, () => {
            this.panelContainer.setVisible(false);
        });
    }"""

new_hide_pause = """    hidePause(callback) {
        this.animateHide(this.pauseContainer, () => {
            this.panelContainer.setVisible(false);
            if (callback) callback();
        });
    }"""

content = content.replace(old_hide_pause, new_hide_pause)

# 3. Update optionsButton handler to use the callback
old_options_button = """        let optionsButton = this.scene.add.image(dim / 2, dim / 2 - 80, 'pantalla_pausa_UI', 'Botón_opciones_NonClicked.png').setInteractive().setDisplaySize(400, 75);
        optionsButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hidePause();
            this.showOptions();
        });"""

new_options_button = """        let optionsButton = this.scene.add.image(dim / 2, dim / 2 - 80, 'pantalla_pausa_UI', 'Botón_opciones_NonClicked.png').setInteractive().setDisplaySize(400, 75);
        optionsButton.on('pointerdown', () => {
            this.scene.audioManager.ui_click.play();
            this.hidePause(() => {
                this.showOptions();
            });
        });"""

content = content.replace(old_options_button, new_options_button)

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(content)

print("Panel refactoring complete.")
