import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    lines = f.readlines()

# Find the start of the corrupted block
start_idx = -1
for i, line in enumerate(lines):
    if 'BreakLine(x, y) {' in line:
        start_idx = i
        break

# Find the end of the corrupted block (next valid logical step)
end_idx = -1
for i in range(start_idx, len(lines)):
    if 'this.audioManager.destruccion.play()' in line:
        # We search specifically for the line that was supposed to follow
        pass

# Let's try a different approach: rewrite from line number to line number
# Based on previous read:
# corrupted part starts at BreakLine(x, y) {
# and seems to end before "this.piecesToClear = []"

new_breakline = [
    "    BreakLine(x, y) {\n",
    "        if (this.linesToClear.length < 1 || this.gamefinish) {\n",
    "            this.FinishTurn();\n",
    "            return;\n",
    "        }\n",
    "        if (this.animationsIterator === 0) {\n",
    "            this.PauseTimer();\n",
    "            // Scaling shake and flash exponentially for TRANSCENDENT impact\n",
    "            let intensity = Math.pow(this.linesToClear.length, 1.5) * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE;\n",
    "            let flashDuration = JUICE_CONFIG.FLASH_DURATION * (1 + this.linesToClear.length * 0.2);\n",
    "            this.cameras.main.shake(JUICE_CONFIG.SHAKE_DURATION, intensity);\n",
    "            this.cameras.main.flash(flashDuration, (JUICE_CONFIG.FLASH_COLOR >> 16) & 0xFF, (JUICE_CONFIG.FLASH_COLOR >> 8) & 0xFF, JUICE_CONFIG.FLASH_COLOR & 0xFF, false);\n",
    "        }\n",
    "\n",
    "        this.piecesToClear = []\n",
    "        this.colorsToRestore = []\n",
    "        this.lineCounterXadd = [0,0,0,0,0,0,0,0]\n",
    "        this.lineCounterYadd = [0,0,0,0,0,0,0,0]\n",
    "\n"
]

# We'll find the start and find the line that says "this.audioManager.destruccion.play()"
start = -1
end = -1
for i, line in enumerate(lines):
    if 'BreakLine(x, y) {' in line:
        start = i
    if 'this.audioManager.destruccion.play()' in line:
        end = i
        break

if start != -1 and end != -1:
    final_lines = lines[:start] + new_breakline + lines[end:]
    with open('src/scripts/scenes/MainScene.js', 'w') as f:
        f.writelines(final_lines)
    print("Success")
else:
    print(f"Failed to find markers: start={start}, end={end}")
