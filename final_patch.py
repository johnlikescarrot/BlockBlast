import sys

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    with open(path, 'r') as f: content = f.read()

    # Shadows
    content = content.replace(
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);',
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);\n        if (this.ghostContainer.postFX) {\n            this.ghostContainer.postFX.addShadow(0, 2, 0.1, 1, 0x000000, 4, 0.3);\n        }'
    )
    content = content.replace(
        'pointerContainer.y = (this.pY-2*this.LAYOUT.SQUARE_SIZE)-this.pointerAdd',
        'pointerContainer.y = (this.pY-2*this.LAYOUT.SQUARE_SIZE)-this.pointerAdd\n                if (pointerContainer.postFX) {\n                    pointerContainer.postFX.clear();\n                    pointerContainer.postFX.addShadow(0, 5, 0.1, 1, 0x000000, 6, 0.5);\n                }'
    )
    # Glow
    content = content.replace(
        'this.piecesToClear.push(this.idleboard[j][i])',
        'this.piecesToClear.push(this.idleboard[j][i])\n                    if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.addGlow(0xffffff, 2, 0); }'
    )
    content = content.replace(
        'this.piecesToClear.push(this.idleboard[i][j])',
        'this.piecesToClear.push(this.idleboard[i][j])\n                    if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.addGlow(0xffffff, 2, 0); }'
    )
    content = content.replace(
        'console.log(this.colorsToRestore[i])',
        'if (this.piecesToClear[i].postFX) { this.piecesToClear[i].postFX.clear(); }\n            console.log(this.colorsToRestore[i])'
    )
    # BreakLine FX + Zoom Reset Fix
    content = content.replace(
        'if (this.animationsIterator === 0) {',
        'if (this.animationsIterator === 0) {\n            let comboCount = this.linesToClear.length;\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;\n            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);'
    )
    content = content.replace(
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);',
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);'
    )
    content = content.replace(
        'this.cameras.main.flash(JUICE_CONFIG.FLASH_DURATION, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);',
        'this.cameras.main.flash(JUICE_CONFIG.FLASH_DURATION, 255, 255, 255, false);'
    )
    content = content.replace(
        'this.RecountLineCounters()',
        'this.RecountLineCounters()\n            this.cameras.main.zoomTo(1.0, 200, "Sine.easeInOut", true);'
    )
    # Early returns zoom reset
    content = content.replace(
        'if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.FinishTurn();\n            return;\n        }',
        'if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();\n            return;\n        }'
    )
    # Shutdown reset
    content = content.replace(
        'this.uiScene = this.scene.get(\'UIScene\');',
        'this.uiScene = this.scene.get(\'UIScene\');\n        this.events.once(\'shutdown\', () => { this.cameras.main.setZoom(1); });'
    )
    with open(path, 'w') as f: f.write(content)

def patch_panel():
    path = 'src/scripts/components/panel.js'
    with open(path, 'r') as f: lines = f.readlines()

    new_lines = []
    skip = 0
    for i, line in enumerate(lines):
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
            skip = 5
        elif 'if (this.scene.currentScene && !this.blurFX) {' in line:
            new_lines.append('        if (this.scene.currentScene && !this.blurFX) {\n')
            new_lines.append('            this.blurFX = this.scene.currentScene.cameras.main.postFX?.addBlur?.(UI_CONFIG.BLUR_QUALITY, UI_CONFIG.BLUR_X, UI_CONFIG.BLUR_Y, 0);\n')
            new_lines.append('            this.scene.tweens.add({\n')
            new_lines.append('                targets: this.blurFX,\n')
            new_lines.append('                strength: UI_CONFIG.BLUR_STRENGTH,\n')
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
            new_lines.append('                strength: 0,\n')
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

patch_main_scene()
patch_panel()
