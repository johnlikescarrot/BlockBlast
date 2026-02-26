import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    lines = f.readlines()

start_index = -1
end_index = -1

for i, line in enumerate(lines):
    if 'if (this.linesToClear.length >= JUICE_CONFIG.COMBO_THRESHOLD) {' in line and 'if (this.animationsIterator === 0) {' in lines[i-7]:
        start_index = i
        # Find the end of this if block
        brace_count = 1
        for j in range(i + 1, len(lines)):
            brace_count += lines[j].count('{')
            brace_count -= lines[j].count('}')
            if brace_count == 0:
                end_index = j + 1
                break
        break

if start_index != -1 and end_index != -1:
    new_block = [
        '            if (this.linesToClear.length >= JUICE_CONFIG.COMBO_THRESHOLD) {\n',
        '                if (this.bloomTimer) {\n',
        '                    this.bloomTimer.remove();\n',
        '                    this.bloomTimer = null;\n',
        '                }\n',
        '                if (this.comboBloom) {\n',
        '                    this.tweens.killTweensOf(this.comboBloom);\n',
        '                    this.boardContainer?.postFX?.remove?.(this.comboBloom);\n',
        '                    this.comboBloom = null;\n',
        '                }\n',
        '                \n',
        '                // Dynamic strength based on number of lines\n',
        '                const dynamicStrength = JUICE_CONFIG.BLOOM_STRENGTH + (this.linesToClear.length - JUICE_CONFIG.COMBO_THRESHOLD);\n',
        '                \n',
        '                this.comboBloom = this.boardContainer?.postFX?.addBloom?.(\n',
        '                    JUICE_CONFIG.BLOOM_COLOR,\n',
        '                    JUICE_CONFIG.BLOOM_BLUR_X,\n',
        '                    JUICE_CONFIG.BLOOM_BLUR_Y,\n',
        '                    dynamicStrength,\n',
        '                    JUICE_CONFIG.BLOOM_STEPS\n',
        '                );\n',
        '                \n',
        '                if (this.comboBloom) {\n',
        '                    const activeBloom = this.comboBloom; // Capture local reference\n',
        '                    this.bloomTimer = this.time.delayedCall(JUICE_CONFIG.COMBO_BLOOM_DURATION, () => {\n',
        '                        this.tweens.add({\n',
        '                            targets: activeBloom,\n',
        '                            strength: 0,\n',
        '                            duration: 200,\n',
        '                            onComplete: () => {\n',
        '                                this.boardContainer?.postFX?.remove?.(activeBloom);\n',
        '                                if (this.comboBloom === activeBloom) {\n',
        '                                    this.comboBloom = null;\n',
        '                                }\n',
        '                                this.bloomTimer = null;\n',
        '                            }\n',
        '                        });\n',
        '                    });\n',
        '                }\n',
        '            }\n'
    ]
    lines[start_index:end_index] = new_block
    with open('src/scripts/scenes/MainScene.js', 'w') as f:
        f.writelines(lines)
    print("Successfully updated bloom logic.")
else:
    print("Could not find bloom logic block.")
    sys.exit(1)
