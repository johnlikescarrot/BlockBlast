import sys, re

def robust_sub(pattern, replacement, content, count=0):
    new_content, n = re.subn(pattern, replacement, content, count=count)
    if n == 0:
        print(f"CRITICAL: Pattern not found: {repr(pattern)}")
        sys.exit(1)
    return new_content

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    with open(path, 'r') as f: content = f.read()

    # 1. Camera Zoom Lifecycle
    content = robust_sub(
        r"this\.uiScene = this\.scene\.get\('UIScene'\);",
        "this.uiScene = this.scene.get('UIScene');\n        this.events.once('shutdown', () => { this.cameras.main.setZoom(1); });",
        content
    )

    # 2. BreakLine - Early return zoom reset
    content = robust_sub(
        r"BreakLine\(x, y\) \{\s+if \(this\.linesToClear\.length < 1 \|\| this\.gamefinish\) \{\s+this\.FinishTurn\(\);",
        "BreakLine(x, y) {\n        if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();",
        content
    )

    # 3. BreakLine - Dynamic Zoom-in and Shake
    content = robust_sub(
        r"if \(this\.animationsIterator === 0\) \{\s+this\.PauseTimer\(\);",
        'if (this.animationsIterator === 0) {\n            let comboCount = this.linesToClear.length;\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;\n            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);\n            this.PauseTimer();',
        content
    )

    # 4. BreakLine - Replace manual shake
    content = robust_sub(
        r"let intensity = this\.linesToClear\.length \* JUICE_CONFIG\.SHAKE_INTENSITY_PER_LINE;\s+this\.cameras\.main\.shake\(JUICE_CONFIG\.SHAKE_DURATION, intensity\);",
        "this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);",
        content
    )

    # 5. BreakLine - Zoom-out on completion
    content = robust_sub(
        r"(this\.RecountLineCounters\(\))\s+this\.PauseTimer\(\)",
        r"\1\n            this.cameras.main.zoomTo(1.0, 200, 'Sine.easeInOut', true);\n            this.PauseTimer()",
        content, count=1
    )

    # 6. Glow Management - Intersection aware
    content = robust_sub(
        r"(this\.piecesToClear\.push\(this\.idleboard\[j\]\[i\]\))",
        r"\1\n                    if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.clear(); this.idleboard[j][i].postFX.addGlow(0xffffff, 2, 0); }",
        content, count=1
    )
    content = robust_sub(
        r"(this\.piecesToClear\.push\(this\.idleboard\[i\]\[j\]\))",
        r"\1\n                    if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.clear(); this.idleboard[i][j].postFX.addGlow(0xffffff, 2, 0); }",
        content, count=1
    )
    content = robust_sub(
        r"(console\.log\(this\.colorsToRestore\[i\]\))",
        r"if (this.piecesToClear[i].postFX) { this.piecesToClear[i].postFX.clear(); }\n            \1",
        content
    )

    # 7. Optimized Shadows - No per-frame recreation
    content = robust_sub(
        r"(this\.ghostContainer = this\.add\.container\(0, 0\)\.setDepth\(2\)\.setAlpha\(JUICE_CONFIG\.GHOST_ALPHA\);)",
        r"\1\n        if (this.ghostContainer.postFX) { this.ghostContainer.postFX.addShadow(0, 2, 0.1, 1, 0x000000, 4, 0.3); }",
        content
    )
    # Flexible regex for dragstart
    content = robust_sub(
        r"(pointerContainer\.visible = true;?\s+this\.canCheck = true)",
        r"if (pointerContainer.postFX) { pointerContainer.postFX.clear(); pointerContainer.postFX.addShadow(0, 5, 0.1, 1, 0x000000, 6, 0.5); }\n                \1",
        content, count=1
    )

    with open(path, 'w') as f: f.write(content)

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
            new_lines.append('    }\n') # Syntax fix: restore closing brace
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
