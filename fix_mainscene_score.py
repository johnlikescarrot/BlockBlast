import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix the stroke call right after label creation
    if "this.scoreLabelText = this.add.text(200, 80, this.uiScene.i18n.t('SCORE')" in line:
        new_lines.append(line)
        # Skip the next line which is the broken stroke call and replace it
        new_lines.append("        this.scoreLabelText.setStroke('#553b37', 8);\n")
        new_lines.append("        this.scoreValueText = this.add.text(200, 140, '00000000', { fontFamily: 'Bungee', fontSize: '40px', color: '#f0dfa7', align: 'center' }).setOrigin(0.5).setDepth(4);\n")
        new_lines.append("        this.scoreValueText.setStroke('#3f2e29', 10);\n")
        continue
    if "this.scoreText.setStroke('#553b37', 8);" in line and i > 1970:
        continue # Already handled
    new_lines.append(line)

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.writelines(new_lines)
