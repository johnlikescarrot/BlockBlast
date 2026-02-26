import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    content = f.read()

# The target block to replace is the entire BreakLine function
# We'll use a marker-based replacement

new_func = """    BreakLine(x, y) {
        if (this.linesToClear.length < 1 || this.gamefinish) {
            this.FinishTurn();
            return;
        }
        if (this.animationsIterator === 0) {
            this.PauseTimer();
            // Scaling shake and flash exponentially for TRANSCENDENT impact
            let intensity = Math.pow(this.linesToClear.length, 1.5) * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE;
            let flashDuration = JUICE_CONFIG.FLASH_DURATION * (1 + this.linesToClear.length * 0.2);
            this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);
            this.cameras.main.flash(flashDuration, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);
        }

        this.piecesToClear = []
        this.colorsToRestore = []
        this.lineCounterXadd = [0,0,0,0,0,0,0,0]
        this.lineCounterYadd = [0,0,0,0,0,0,0,0]

        this.audioManager.destruccion.play()"""

# We search for the corrupted start and replace until the next unique anchor
start_marker = "BreakLine(x, y) {"
end_marker = "this.audioManager.destruccion.play()"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + new_func + content[end_idx + len(end_marker):]
    with open('src/scripts/scenes/MainScene.js', 'w') as f:
        f.write(new_content)
    print("Success")
else:
    print(f"Markers not found: start={start_idx}, end={end_idx}")
