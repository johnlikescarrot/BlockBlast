import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_next = 0
for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue

    if "this.scoreLabelText = this.add.text(200, 80, this.uiScene.i18n.t('SCORE'), {" in line:
        new_lines.append("        this.scoreLabelText = this.add.text(200, 80, this.uiScene.i18n.t('SCORE'), { \n")
        new_lines.append("            fontFamily: 'Bungee', fontSize: '60px', color: '#f4f4f4', align: 'center' }).setOrigin(0.5).setDepth(4);\n")
        new_lines.append("        this.scoreLabelText.setStroke('#553b37', 8);\n")
        new_lines.append("        this.scoreValueText = this.add.text(200, 140, '00000000', { \n")
        new_lines.append("            fontFamily: 'Bungee', fontSize: '40px', color: '#f0dfa7', align: 'center' }).setOrigin(0.5).setDepth(4);\n")
        new_lines.append("        this.scoreValueText.setStroke('#3f2e29', 10);\n")
        # I need to find how many lines to skip. The previous broken script added some junk.
        # Let's look at the next few lines.
        j = i + 1
        while j < len(lines) and ("fontFamily" in lines[j] or "this.scoreText.setStroke" in lines[j] or "this.scoreLabelText.setStroke" in lines[j] or "this.scoreValueText" in lines[j]):
             j += 1
        skip_next = j - i - 1
        continue

    new_lines.append(line)

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.writelines(new_lines)
