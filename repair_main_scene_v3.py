import os

path = 'src/scripts/scenes/MainScene.js'
with open(path, 'r') as f:
    content = f.read()

# Fix the second glow loop in ShowBreakingLines
old_glow_y = 'if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.clear(); this.idleboard[i][j].postFX.addGlow(0xffffff, 2, 0); }'
new_glow_y = 'if (this.idleboard[i][j].postFX) { this.idleboard[i][j].postFX.clear(); this.idleboard[i][j].postFX.addGlow(JUICE_CONFIG.LINE_CLEAR_GLOW_COLOR, 2, 0); }'
content = content.replace(old_glow_y, new_glow_y)

with open(path, 'w') as f:
    f.write(content)
