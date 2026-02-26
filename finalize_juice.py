import re

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    content = f.read()

# 1. Batch landing bounce tweens in InsertPiece
insert_piece_pattern = r'(InsertPiece\(piece,x,y\)\{.*?this\.audioManager\.soltar\.play\(\))(.*?)(console\.log\("CHECK)'
def batch_tweens(match):
    header = match.group(1)
    body = match.group(2)
    footer = match.group(3)

    # Add target array initialization
    header += '\n        const landingBounceTargets = [];'

    # Replace individual tween with push
    new_body = re.sub(
        r'// Landing bounce effect\s+this\.tweens\.add\(\{\s+targets: \[this\.board\[j\+x\]\[i\+y\], this\.idleboard\[j\+x\]\[i\+y\]\],\s+scale: \{ from: 1\.2, to: 1 \},\s+duration: JUICE_CONFIG\.LAND_BOUNCE_DURATION,\s+ease: \'Bounce\.easeOut\'\s+\}\);',
        'landingBounceTargets.push(this.board[j+x][i+y], this.idleboard[j+x][i+y]);',
        body, flags=re.DOTALL
    )

    # Add the single tween call before footer
    new_body += '\n        if (landingBounceTargets.length) {\n            this.tweens.add({\n                targets: landingBounceTargets,\n                scale: { from: 1.2, to: 1 },\n                duration: JUICE_CONFIG.LAND_BOUNCE_DURATION,\n                ease: "Bounce.easeOut"\n            });\n        }\n        '

    return header + new_body + footer

content = re.sub(insert_piece_pattern, batch_tweens, content, flags=re.DOTALL)

# 2. Finalize bloom logic with safe cleanup (already partially done, but let's ensure it's clean)
# My previous update_bloom.py used activeBloom, which is correct.
# I'll just check if there's any duplicate cleanup code.

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.write(content)
print("Finalized juice optimizations.")
