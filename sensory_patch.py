import sys, re

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    with open(path, 'r') as f: content = f.read()

    # 1. Initialize Sensory FX in create
    content = content.replace(
        "this.uiScene = this.scene.get('UIScene');",
        "this.uiScene = this.scene.get('UIScene');\n        this.vignette = this.cameras.main.postFX.addVignette(0.5, 0.5, 0.8, 0);\n        this.barrel = this.cameras.main.postFX.addBarrel(1.0);\n        this.barrel.setActive(false);"
    )

    # 2. Pulsing Vignette in update
    vignette_logic = """
        // Transcendent Pulse Logic
        if (this.timeSlider && this.timeSlider.value <= 0.3) {
            let pulse = Math.abs(Math.sin(time * 0.01)) * 0.4;
            this.vignette.strength = 0.3 + pulse;
        } else {
            this.vignette.strength = Phaser.Math.Linear(this.vignette.strength, 0, 0.1);
        }
    """
    content = content.replace(
        "this.updateGhostPiece(this.pointerX, this.pointerY, this.piece.shape);",
        "this.updateGhostPiece(this.pointerX, this.pointerY, this.piece.shape);" + vignette_logic
    )

    # 3. Dynamic Audio and Shockwave in BreakLine
    content = content.replace(
        "this.audioManager.destruccion.play()",
        "this.audioManager.destruccion.play({ detune: comboCount * 100 });\n        this.barrel.setActive(true);\n        this.barrel.amount = 1.02;\n        this.time.delayedCall(200, () => { this.barrel.amount = 1.0; this.barrel.setActive(false); });"
    )

    # 4. Camera Thud on Insert
    content = content.replace(
        "this.cameras.main.shake(JUICE_CONFIG.LAND_SHAKE_DURATION, JUICE_CONFIG.LAND_SHAKE_INTENSITY);",
        "this.cameras.main.shake(JUICE_CONFIG.LAND_SHAKE_DURATION, JUICE_CONFIG.LAND_SHAKE_INTENSITY);\n                    this.cameras.main.setScroll(0, -5);\n                    this.time.delayedCall(50, () => this.cameras.main.setScroll(0, 0));"
    )

    # 5. Restore definitive fixes from previous step to ensure integrity
    # (Shadows, Glows, Zoom Integrity)
    content = content.replace(
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);',
        'this.ghostContainer = this.add.container(0, 0).setDepth(2).setAlpha(JUICE_CONFIG.GHOST_ALPHA);\n        if (this.ghostContainer.postFX) {\n            this.ghostContainer.postFX.addShadow(0, 2, 0.1, 1, 0x000000, 4, 0.3);\n        }'
    )
    content = re.sub(
        r'(pointerContainer\.visible = true;?\s+this\.canCheck = true)',
        r'if (pointerContainer.postFX) { pointerContainer.postFX.clear(); pointerContainer.postFX.addShadow(0, 5, 0.1, 1, 0x000000, 6, 0.5); }\n                \1',
        content, count=1
    )
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
    content = content.replace(
        'if (this.animationsIterator === 0) {',
        'if (this.animationsIterator === 0) {\n            let comboCount = this.linesToClear.length;\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;\n            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);'
    )
    content = content.replace(
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);',
        'this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);'
    )
    content = content.replace(
        'this.RecountLineCounters()',
        'this.RecountLineCounters()\n            this.cameras.main.zoomTo(1.0, 200, "Sine.easeInOut", true);',
        1
    )
    content = re.sub(
        r'if \(this\.linesToClear\.length < 1 \|\| this\.gamefinish\) \{\s+this\.FinishTurn\(\);',
        'if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();',
        content
    )
    content = content.replace(
        "this.uiScene = this.scene.get('UIScene');",
        "this.uiScene = this.scene.get('UIScene');\n        this.events.once('shutdown', () => { this.cameras.main.setZoom(1); });"
    )

    with open(path, 'w') as f: f.write(content)

patch_main_scene()
