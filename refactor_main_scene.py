import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    lines = f.readlines()

# Define the new method
new_method = [
    "    blinkTimerIndicator(indicator) {\n",
    "        this.tweens.add({\n",
    "            targets: indicator,\n",
    "            alpha: 0.5,\n",
    "            duration: 100,\n",
    "            yoyo: true,\n",
    "            onComplete: () => indicator.setAlpha(1)\n",
    "        });\n",
    "    }\n",
    "\n"
]

# Find the insertion point (before ShowTime)
insertion_idx = -1
for i, line in enumerate(lines):
    if 'ShowTime(){' in line:
        insertion_idx = i
        break

if insertion_idx != -1:
    lines[insertion_idx:insertion_idx] = new_method

# Find and replace the duplicated logic
# Note: insertion_idx shifted the line numbers for subsequent checks
new_lines = []
for line in lines:
    if 'this.tweens.add({ targets: indicator, alpha: 0.5, duration: 100, yoyo: true, onComplete: () => indicator.setAlpha(1) });' in line:
        new_lines.append(line.replace('this.tweens.add({ targets: indicator, alpha: 0.5, duration: 100, yoyo: true, onComplete: () => indicator.setAlpha(1) });', 'this.blinkTimerIndicator(indicator);'))
    else:
        new_lines.append(line)

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.writelines(new_lines)

print("Refactoring complete.")
