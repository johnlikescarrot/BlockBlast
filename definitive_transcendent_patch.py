import os
import re
import sys
import subprocess

def robust_sub(pattern, replacement, content, count=0, literal=False):
    if literal:
        pattern = re.escape(pattern)
    new_content, n = re.subn(pattern, replacement, content, count=count)
    return new_content, n

def verify_js(path):
    try:
        subprocess.run(['node', '--check', path], check=True, capture_output=True)
        print(f"Verified syntax for {path}")
    except subprocess.CalledProcessError as e:
        print(f"SYNTAX ERROR in {path}:")
        print(e.stderr.decode())
        sys.exit(1)

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    if "// Transcendent Fixed Scoping" not in content:
        content, n = robust_sub(
            r'BreakLine\(x, y\) \{([\s\S]*?)let comboCount = this\.linesToClear\.length;',
            'BreakLine(x, y) {\n        // Transcendent Fixed Scoping\n        if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();\n            return;\n        }\n        let comboCount = this.linesToClear.length;',
            content, count=1
        )
        if n > 0: changed = True

    # Scoped shakeIntensity check
    if 'let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;' in content:
        # Check if it's inside the if block
        match = re.search(r'if \(this\.animationsIterator === 0\) \{\s+let shakeIntensity', content)
        if not match:
            content, n = robust_sub(
                r'let shakeIntensity = comboCount \* JUICE_CONFIG\.SHAKE_INTENSITY_PER_LINE \* 1\.5;\s+if \(this\.animationsIterator === 0\) \{',
                'if (this.animationsIterator === 0) {\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;',
                content, count=1
            )
            if n > 0: changed = True

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
    else:
        print("MainScene: No changes needed.")

def patch_panel():
    path = 'src/scripts/components/panel.js'
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    if "// Transcendent Panel Fixed" not in content:
        content, n = robust_sub(
            'constructor(scene) {',
            'constructor(scene) {\n        // Transcendent Panel Fixed',
            content, count=1, literal=True
        )
        if n > 0: changed = True

    if "BOKEH_RADIUS" not in content:
        content, n = robust_sub(
            'SHOW_DURATION: 600,',
            'SHOW_DURATION: 600,\n    BOKEH_RADIUS: 0.5,\n    BOKEH_AMOUNT: 1.0,\n    BOKEH_CONTRAST: 0,\n    BOKEH_TARGET_RADIUS: 10,',
            content, count=1, literal=True
        )
        if n > 0: changed = True

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
    else:
        print("Panel: No changes needed.")

def patch_uiscene():
    path = 'src/scripts/scenes/UIScene.js'
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    if "// Transcendent UI Fixed" not in content:
        if 'let wipe = this.splashScreen.postFX.addWipe(0.1, 0, 1);' in content:
            content, n = robust_sub(
                r'let wipe = this\.splashScreen\.postFX\.addWipe\(0\.1, 0, 1\); // wipeWidth, direction, axis',
                '// Transcendent UI Fixed\n            let wipe = this.splashScreen.postFX.addWipe(0.1, 1, 0); // wipeWidth, direction, axis',
                content, count=1
            )
            if n > 0: changed = True

            content, n = robust_sub(
                r'if \(this\.splashScreen\.postFX\) this\.splashScreen\.postFX\.remove\(wipe\);',
                'if (this.splashScreen.postFX) this.splashScreen.postFX.clear();',
                content, count=1
            )
            if n > 0: changed = True

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
    else:
        print("UIScene: No changes needed.")

if __name__ == "__main__":
    patch_main_scene()
    patch_panel()
    patch_uiscene()
    print("Robust patching orchestration complete.")
