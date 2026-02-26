import sys, re

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    with open(path, 'r') as f: content = f.read()

    # 1. Shadows
    content = content.replace(
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);',
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);\n        if (this.ghostContainer.postFX) {\n            this.ghostContainer.postFX.addShadow(0, 2, 0.1, 1, 0x000000, 4, 0.3);\n        }'
    )

    # Dragstart shadow
    content = re.sub(
        r'(pointerContainer\.visible = true\s+this\.canCheck = true)',
        r'if (pointerContainer.postFX) { pointerContainer.postFX.clear(); pointerContainer.postFX.addShadow(0, 5, 0.1, 1, 0x000000, 6, 0.5); }\n                \1',
        content, count=1
    )

    # 2. Glow - prevent stacking
    content = content.replace(
        'this.piecesToClear.push(this.idleboard[j][i])',
        'this.piecesToClear.push(this.idleboard[j][i])\n                    if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.clear(); this.idleboard[j][i].postFX.addGlow(0xffffff, 2, 0); }'
    )
    content = content.replace(
        'this.piecesToClear.push(this.idleboard[i][j])',
        'this.piecesToClear.push(this.idleboard[i][j])\n                    if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.clear(); this.idleboard[i][j].postFX.addGlow(0xffffff, 2, 0); }'
    )
    content = content.replace(
        'console.log(this.colorsToRestore[i])',
        'if (this.piecesToClear[i].postFX) { this.piecesToClear[i].postFX.clear(); }\n            console.log(this.colorsToRestore[i])'
    )

    # 3. BreakLine FX
    content = content.replace(
        'if (this.animationsIterator === 0) {',
        'if (this.animationsIterator === 0) {\n            let comboCount = this.linesToClear.length;\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;\n            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);'
    )

    content = content.replace(
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);',
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);'
    )

    # Use regex for the complex flash line
    content = re.sub(
        r'this\.cameras\.main\.flash\(JUICE_CONFIG\.FLASH_DURATION, .*?, false\);',
        'this.cameras.main.flash(JUICE_CONFIG.FLASH_DURATION, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);',
        content
    )

    # Zoom reset only in BreakLine (it's the first occurrence of RecountLineCounters)
    content = content.replace(
        'this.RecountLineCounters()',
        'this.RecountLineCounters()\n            this.cameras.main.zoomTo(1.0, 200, "Sine.easeInOut", true);',
        1
    )

    # 4. Zoom consistency
    content = re.sub(
        r'if \(this\.linesToClear\.length < 1 \|\| this\.gamefinish\) \{\s+this\.FinishTurn\(\);\s+return;\s+\}',
        'if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();\n            return;\n        }',
        content
    )

    content = content.replace(
        "this.uiScene = this.scene.get('UIScene');",
        "this.uiScene = this.scene.get('UIScene');\n        this.events.once('shutdown', () => { this.cameras.main.setZoom(1); });"
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
