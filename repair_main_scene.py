import os

path = 'src/scripts/scenes/MainScene.js'
with open(path, 'r') as f:
    content = f.read()

# 1. Fix BreakLine: comboCount scope, hardcoded values, and barrel FX
old_breakline = """    BreakLine(x, y) {
        // Transcendent Fixed Scoping
        if (this.linesToClear.length < 1 || this.gamefinish) {
            this.cameras.main.setZoom(1);
            this.FinishTurn();
            return;
        }
        let comboCount = this.linesToClear.length;
        if (this.animationsIterator === 0) {
            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;
            this.cameras.main.zoomTo(1.05, 100, "Sine.easeInOut", true);
            this.PauseTimer();
            this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);
            this.cameras.main.flash(JUICE_CONFIG.FLASH_DURATION, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);

            if (this.linesToClear.length >= JUICE_CONFIG.COMBO_THRESHOLD) {"""

new_breakline = """    BreakLine(x, y) {
        let comboCount = this.linesToClear.length;
        // Transcendent Fixed Scoping
        if (comboCount < 1 || this.gamefinish) {
            this.cameras.main.setZoom(1);
            this.FinishTurn();
            return;
        }
        if (this.animationsIterator === 0) {
            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;
            this.cameras.main.zoomTo(JUICE_CONFIG.TRANS_ZOOM, 100, "Sine.easeInOut", true);
            this.PauseTimer();
            this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, shakeIntensity);
            this.cameras.main.flash(JUICE_CONFIG.FLASH_DURATION, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);

            if (comboCount >= JUICE_CONFIG.COMBO_THRESHOLD) {"""

content = content.replace(old_breakline, new_breakline)

# 2. Fix the barrel logic inside BreakLine
old_barrel_logic = """        this.audioManager.destruccion.play({ detune: comboCount * 100 });
        if (this.barrel) { this.barrel.setActive(true); this.barrel.amount = 1.02; this.time.delayedCall(200, () => { if (this.barrel) { this.barrel.amount = 1.0; this.barrel.setActive(false); } }); }"""

new_barrel_logic = """        this.audioManager.destruccion.play({ detune: comboCount * 100 });
        if (this.barrel) {
            this.barrel.amount = 1.0 + (JUICE_CONFIG.BARREL_STRENGTH * 0.1);
            this.time.delayedCall(200, () => { if (this.barrel) this.barrel.amount = 1.0; });
        }"""

content = content.replace(old_barrel_logic, new_barrel_logic)

with open(path, 'w') as f:
    f.write(content)
