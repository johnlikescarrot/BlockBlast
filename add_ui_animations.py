import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    content = f.read()

# Logic to add floating tweens for each option
floating_tween_logic = """
        // Transcendent Floating Animation for Piece Options
        [this.option1, this.option2, this.option3].forEach((option, index) => {
            if (option) {
                this.tweens.add({
                    targets: option,
                    y: option.y - 10,
                    duration: 1500 + (index * 200),
                    yoyo: true,
                    repeat: -1,
                    ease: 'Sine.easeInOut'
                });
            }
        });
"""

# Insert before "this.currentTime = this.maxTimePerTurn" in CreateOptions
content = content.replace("this.currentTime = this.maxTimePerTurn", floating_tween_logic + "\n        this.currentTime = this.maxTimePerTurn")

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.write(content)

# Enhancing Panel.js easing
with open('src/scripts/components/panel.js', 'r') as f:
    panel_content = f.read()

panel_content = panel_content.replace("duration: 600,", "duration: 800,")
panel_content = panel_content.replace("ease: 'Elastic.easeOut',", "ease: 'Elastic.easeOut',\\n            easeParams: [1.2, 0.6]")

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(panel_content)

print("Success")
