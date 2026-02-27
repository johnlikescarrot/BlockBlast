import os

path = 'src/scripts/scenes/MainScene.js'
with open(path, 'r') as f:
    content = f.read()

# 1. Update JUICE_CONFIG for better multiplier management
content = content.replace(
    'PITCH_SHIFT_MAX: 1200',
    'PITCH_SHIFT_MAX: 1200,\n    SHAKE_MULTIPLIER: 1.5,\n    LINE_CLEAR_GLOW_COLOR: 0xffffff'
)

# 2. Use SHAKE_MULTIPLIER in BreakLine
content = content.replace(
    'let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;',
    'let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * JUICE_CONFIG.SHAKE_MULTIPLIER;'
)

# 3. Add detune logic to gameplayMusic with safety check
old_play_sound = 'this.audioManager.destruccion.play({ detune: comboCount * 100 });'
new_play_sound = """        this.audioManager.destruccion.play({ detune: comboCount * 100 });
        if (this.audioManager.gameplayMusic) {
            this.audioManager.gameplayMusic.setDetune(Math.min(comboCount * 200, JUICE_CONFIG.PITCH_SHIFT_MAX));
            this.time.delayedCall(1000, () => {
                if (this.audioManager.gameplayMusic) this.audioManager.gameplayMusic.setDetune(0);
            });
        }"""
content = content.replace(old_play_sound, new_play_sound)

# 4. Fix glow stacking in ShowBreakingLines and use config
old_glow_x = 'if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.clear(); this.idleboard[j][i].postFX.addGlow(0xffffff, 2, 0); }'
new_glow_x = 'if (this.idleboard[j][i].postFX) { this.idleboard[j][i].postFX.clear(); this.idleboard[j][i].postFX.addGlow(JUICE_CONFIG.LINE_CLEAR_GLOW_COLOR, 2, 0); }'
content = content.replace(old_glow_x, new_glow_x)

# Note: The original file has two loops for glow.
# Let me check if both were using the same literal.

with open(path, 'w') as f:
    f.write(content)
