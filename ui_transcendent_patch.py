import sys

def patch_panel():
    path = 'src/scripts/components/panel.js'
    with open(path, 'r') as f: lines = f.readlines()

    new_lines = []
    skip = 0
    for _i, line in enumerate(lines):
        if skip > 0: skip -= 1; continue
        if 'constructor(scene) {' in line:
            new_lines.append(line)
            new_lines.append('        this.scene = scene;\n')
            new_lines.append('        this.updateCredits();\n')
            new_lines.append('        this._hideInstructionsCallback = null;\n')
            new_lines.append('        this.blurFX = null;\n')
            new_lines.append('        this._onPointerMove = (pointer) => {\n')
            new_lines.append('            if (this.panelContainer && this.panelContainer.visible) {\n')
            new_lines.append('                let centerX = this.scene.cameras.main.width / 2;\n')
            new_lines.append('                let dx = (pointer.x - centerX) / centerX;\n')
            new_lines.append('                this.panelContainer.setRotation(dx * 0.02);\n')
            new_lines.append('            }\n')
            new_lines.append('        };\n')
            new_lines.append('        this.scene.input.on("pointermove", this._onPointerMove);\n')
            new_lines.append('        this.scene.events.once("shutdown", () => {\n')
            new_lines.append('            this.scene.input.off("pointermove", this._onPointerMove);\n')
            new_lines.append('        });\n')
            new_lines.append('    }\n')
            skip = 5
        elif 'if (this.scene.currentScene && !this.blurFX) {' in line:
            new_lines.append('        if (this.scene.currentScene && !this.blurFX) {\n')
            new_lines.append('            // Transcendent Bokeh Transition\n')
            new_lines.append('            this.blurFX = this.scene.currentScene.cameras.main.postFX?.addBokeh?.(0.5, 1.0, 0);\n')
            new_lines.append('            this.scene.tweens.add({\n')
            new_lines.append('                targets: this.blurFX,\n')
            new_lines.append('                radius: 10,\n')
            new_lines.append('                duration: UI_CONFIG.SHOW_DURATION\n')
            new_lines.append('            });\n')
            new_lines.append('        }\n')
            skip = 2
        elif 'animateHide(container, onComplete) {' in line:
            new_lines.append('    animateHide(container, onComplete) {\n')
            new_lines.append('        this.scene.tweens.add({\n')
            new_lines.append('            targets: container,\n')
            new_lines.append('            scale: 0,\n')
            new_lines.append('            duration: UI_CONFIG.HIDE_DURATION,\n')
            new_lines.append('            ease: "Back.easeIn",\n')
            new_lines.append('            onComplete: () => {\n')
            new_lines.append('                container.setVisible(false);\n')
            new_lines.append('                if (onComplete) onComplete();\n')
            new_lines.append('            }\n')
            new_lines.append('        });\n')
            new_lines.append('        if (this.blurFX) {\n')
            new_lines.append('            this.scene.tweens.add({\n')
            new_lines.append('                targets: this.blurFX,\n')
            new_lines.append('                radius: 0,\n')
            new_lines.append('                duration: UI_CONFIG.HIDE_DURATION,\n')
            new_lines.append('                onComplete: () => {\n')
            new_lines.append('                    if (this.blurFX) {\n')
            new_lines.append('                        this.scene.currentScene?.cameras?.main?.postFX?.remove?.(this.blurFX);\n')
            new_lines.append('                        this.blurFX = null;\n')
            new_lines.append('                    }\n')
            new_lines.append('                }\n')
            new_lines.append('            });\n')
            new_lines.append('        }\n')
            new_lines.append('    }\n')
            skip = 15
        else: new_lines.append(line)

    with open(path, 'w') as f: f.writelines(new_lines)

patch_panel()
