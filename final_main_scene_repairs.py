import os

path = 'src/scripts/scenes/MainScene.js'
with open(path, 'r') as f:
    content = f.read()

# 1. Fix Detune Reset safety in CreateOptions (as per review)
# The review mentioned delayedCall detune reset doesn't check if music exists.
# I will find the detune logic and wrap it.

old_detune = """            if (this.audioManager.gameplayMusic) {
                this.audioManager.gameplayMusic.setDetune(Phaser.Math.Clamp(this.linesToClear.length * 200, 0, JUICE_CONFIG.PITCH_SHIFT_MAX));
                this.time.delayedCall(1000, () => this.audioManager.gameplayMusic.setDetune(0));
            }"""

# Actually, my previous cat showed this was NOT in the file yet, it was in the "replace_breakline_juice.txt" which failed.
# Let me check if I actually applied it.
