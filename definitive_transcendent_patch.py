import sys
import re
import subprocess

def robust_sub(pattern, replacement, content, count=0, flags=0):
    new_content, n = re.subn(pattern, replacement, content, count=count, flags=flags)
    if n == 0:
        print(f"CRITICAL: Pattern not found: {pattern!r}")
        sys.exit(1)
    return new_content

def verify_syntax(path):
    print(f"Verifying syntax for {path}...")
    result = subprocess.run(['node', '--check', path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SYNTAX ERROR in {path}:\n{result.stderr}")
        sys.exit(1)
    print(f"Syntax OK for {path}")

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    with open(path, 'r') as f:
        content = f.read()

    # Shadows
    content = robust_sub(
        r'(this\.ghostContainer = this\.add\.container\(0, 0\)\.setDepth\(2\)\.setAlpha\(JUICE_CONFIG\.GHOST_ALPHA\);)',
        r'\1\n        if (this.ghostContainer.postFX) { this.ghostContainer.postFX.addShadow(0, 2, 0.1, 1, 0x000000, 4, 0.3); }',
        content
    )

    # Shadows on drag
    content = robust_sub(
        r'(pointerContainer\.visible = true;?\s+this\.canCheck = true)',
        r'if (pointerContainer.postFX) { pointerContainer.postFX.clear(); pointerContainer.postFX.addShadow(0, 5, 0.1, 1, 0x000000, 6, 0.5); }\n                \1',
        content, count=1
    )

    # Glow
    content = robust_sub(
        r'(this\.piecesToClear\.push\(this\.idleboard\[j\]\[i\]\))',
        r'\1\n                    if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.clear(); this.idleboard[j][i].postFX.addGlow(0xffffff, 2, 0); }',
        content, count=1
    )
    content = robust_sub(
        r'(this\.piecesToClear\.push\(this\.idleboard\[i\]\[j\]\))',
        r'\1\n                    if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.clear(); this.idleboard[i][j].postFX.addGlow(0xffffff, 2, 0); }',
        content, count=1
    )
    content = robust_sub(
        r'(console\.log\(this\.colorsToRestore\[i\]\))',
        r'if (this.piecesToClear[i].postFX) { this.piecesToClear[i].postFX.clear(); }\n            \1',
        content
    )

    # BreakLine
    content = robust_sub(
        r"this\.uiScene = this\.scene\.get\('UIScene'\);",
        "this.uiScene = this.scene.get('UIScene');\n        this.vignette = this.cameras?.main?.postFX ? this.cameras.main.postFX.addVignette(0.5, 0.5, 0.8, 0) : null;\n        this.barrel = this.cameras?.main?.postFX ? this.cameras.main.postFX.addBarrel(1.0) : null;\n        this.barrel?.setActive(false);\n        this.events.once('shutdown', () => { this.cameras.main.setZoom(1); });",
        content
    )

    # Hoist variables to method scope to avoid ReferenceErrors
    content = robust_sub(
        r'BreakLine\(x, y\) \{',
        'BreakLine(x, y) {\n        let comboCount = this.linesToClear.length;\n        let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;',
        content
    )

    content = robust_sub(
        r'if \(this\.animationsIterator === 0\) \{',
        'if (this.animationsIterator === 0) {\n            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);',
        content
    )

    content = robust_sub(
        r"this\.audioManager\.destruccion\.play\(\)",
        "this.audioManager.destruccion.play({ detune: comboCount * 100 });\n        if (this.barrel) { this.barrel.setActive(true); this.barrel.amount = 1.02; this.time.delayedCall(200, () => { if (this.barrel) { this.barrel.amount = 1.0; this.barrel.setActive(false); } }); }",
        content
    )

    content = robust_sub(
        r"let intensity = this\.linesToClear\.length \* JUICE_CONFIG\.SHAKE_INTENSITY_PER_LINE;\s+this\.cameras\.main\.shake\(JUICE_CONFIG\.SHAKE_DURATION, intensity\);",
        "this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);",
        content
    )

    content = robust_sub(
        r"(this\.RecountLineCounters\(\))\s+this\.PauseTimer\(\)",
        r"\1\n            this.cameras.main.zoomTo(1.0, 200, 'Sine.easeInOut', true);\n            this.PauseTimer()",
        content, count=1
    )

    content = robust_sub(
        r'if \(this\.linesToClear\.length < 1 \|\| this\.gamefinish\) \{([\s\n]+)this\.FinishTurn\(\);',
        r'if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\1this.FinishTurn();',
        content
    )

    content = robust_sub(
        r"this\.cameras\.main\.shake\(JUICE_CONFIG\.LAND_SHAKE_DURATION, JUICE_CONFIG\.LAND_SHAKE_INTENSITY\);",
        "this.cameras.main.shake(JUICE_CONFIG.LAND_SHAKE_DURATION, JUICE_CONFIG.LAND_SHAKE_INTENSITY);\n                    this.cameras.main.setScroll(0, -5);\n                    this.time.delayedCall(50, () => this.cameras.main.setScroll(0, 0));",
        content
    )

    content = robust_sub(
        r"(this\.updateGhostPiece\(this\.pointerX, this\.pointerY, this\.piece\.shape\);)",
        r"\1\n        if (this.vignette && this.timeSlider && this.timeSlider.value <= 0.3) {\n            let pulse = Math.abs(Math.sin(time * 0.01)) * 0.4;\n            this.vignette.strength = 0.3 + pulse;\n        } else if (this.vignette) {\n            this.vignette.strength = Phaser.Math.Linear(this.vignette.strength, 0, 0.1);\n        }",
        content
    )

    with open(path, 'w') as f:
        f.write(content)
    verify_syntax(path)

def patch_panel():
    path = 'src/scripts/components/panel.js'
    with open(path, 'r') as f:
        content = f.read()

    # Config
    content = robust_sub(
        r'const UI_CONFIG = \{.*?\};',
        'const UI_CONFIG = {\n    SHOW_DURATION: 600,\n    HIDE_DURATION: 300,\n    BOKEH_RADIUS: 0.5,\n    BOKEH_AMOUNT: 1.0,\n    BOKEH_CONTRAST: 0,\n    BOKEH_TARGET_RADIUS: 10\n};',
        content, count=1, flags=re.DOTALL
    )

    # Constructor - fix: matching until next method to ensure balanced braces
    content = robust_sub(
        r'constructor\(scene\) \{.*?\}\s+animateShow',
        'constructor(scene) {\n        this.scene = scene;\n        this.updateCredits();\n        this._hideInstructionsCallback = null;\n        this.blurFX = null;\n        this._onPointerMove = (pointer) => {\n            if (this.panelContainer && this.panelContainer.visible) {\n                let centerX = this.scene.cameras.main.width / 2;\n                let dx = (pointer.x - centerX) / centerX;\n                this.panelContainer.setRotation(dx * 0.02);\n            }\n        };\n        this.scene.input.on("pointermove", this._onPointerMove);\n        this.scene.events.once("shutdown", () => {\n            this.scene.input.off("pointermove", this._onPointerMove);\n        });\n    }\n\n    animateShow',
        content, count=1, flags=re.DOTALL
    )

    content = robust_sub(
        r'if \(this\.scene\.currentScene && !this\.blurFX\) \{.*?\}',
        'if (this.scene.currentScene && !this.blurFX) {\n            // Transcendent Bokeh Transition\n            this.blurFX = this.scene.currentScene.cameras.main.postFX?.addBokeh?.(UI_CONFIG.BOKEH_RADIUS, UI_CONFIG.BOKEH_AMOUNT, UI_CONFIG.BOKEH_CONTRAST);\n            if (this.blurFX) {\n                this.scene.tweens.add({\n                    targets: this.blurFX,\n                    radius: UI_CONFIG.BOKEH_TARGET_RADIUS,\n                    duration: UI_CONFIG.SHOW_DURATION\n                });\n            }\n        }',
        content, count=1, flags=re.DOTALL
    )

    # animateHide - refined regex
    content = robust_sub(
        r'animateHide\(container, onComplete\) \{.*?\}\s+updateCredits\(\)',
        'animateHide(container, onComplete) {\n        this.scene.tweens.add({\n            targets: container,\n            scale: 0,\n            duration: UI_CONFIG.HIDE_DURATION,\n            ease: "Back.easeIn",\n            onComplete: () => {\n                container.setVisible(false);\n                if (onComplete) onComplete();\n            }\n        });\n        if (this.blurFX) {\n            this.scene.tweens.add({\n                targets: this.blurFX,\n                radius: 0,\n                duration: UI_CONFIG.HIDE_DURATION,\n                onComplete: () => {\n                    if (this.blurFX) {\n                        this.scene.currentScene?.cameras?.main?.postFX?.remove?.(this.blurFX);\n                        this.blurFX = null;\n                    }\n                }\n            });\n        }\n    }\n\n    updateCredits()',
        content, count=1, flags=re.DOTALL
    )

    with open(path, 'w') as f:
        f.write(content)
    verify_syntax(path)

def patch_uiscene():
    path = 'src/scripts/scenes/UIScene.js'
    with open(path, 'r') as f:
        content = f.read()

    content = robust_sub(
        r'splashScreenAnim\(\)\{.*?\}\s+setCurrentScene',
        'splashScreenAnim(){\n        this.graphics.setVisible(true);\n        this.splashScreen.setAlpha(1);\n        if (this.splashScreen.postFX) {\n            let wipe = this.splashScreen.postFX.addWipe(0.1, 0, 1); // wipeWidth, direction, axis\n            this.tweens.add({\n                targets: wipe,\n                progress: 1,\n                duration: 1000,\n                ease: "Quint.easeOut",\n                onComplete: () => {\n                    this.time.delayedCall(UI_CONFIG.SPLASH_DELAY, () => {\n                        this.tweens.add({\n                            targets: wipe,\n                            progress: 0,\n                            duration: 800,\n                            ease: "Quint.easeIn",\n                            onComplete: () => {\n                                if (this.splashScreen.postFX) this.splashScreen.postFX.remove(wipe);\n                                this.graphics.setVisible(false);\n                                this.splashScreen.setVisible(false);\n                            }\n                        });\n                    });\n                }\n            });\n        } else {\n            this.time.delayedCall(UI_CONFIG.SPLASH_DELAY + 1000, () => {\n                this.graphics.setVisible(false);\n                this.splashScreen.setVisible(false);\n            });\n        }\n    }\n\n    setCurrentScene',
        content, count=1, flags=re.DOTALL
    )

    with open(path, 'w') as f:
        f.write(content)
    verify_syntax(path)

if __name__ == "__main__":
    patch_main_scene()
    patch_panel()
    patch_uiscene()
    print("PATCH COMPLETED AND VERIFIED.")
