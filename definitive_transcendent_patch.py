import os
import re
import sys

def robust_sub(pattern, replacement, content, count=0):
    new_content, n = re.subn(pattern, replacement, content, count=count)
    if n == 0:
        print(f"CRITICAL: Pattern not found: {pattern!r}")
        sys.exit(1)
    return new_content

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()

    # Idempotency check
    if "// Transcendent Fixed Scoping" in content:
        print("MainScene already patched.")
    else:
        content = robust_sub(
            r'BreakLine\(x, y\) \{',
            'BreakLine(x, y) {\n        // Transcendent Fixed Scoping\n        if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();\n            return;\n        }\n        let comboCount = this.linesToClear.length;',
            content, count=1
        )
        with open(path, 'w') as f: f.write(content)

def patch_panel():
    path = 'src/scripts/components/panel.js'
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()

    if "// Transcendent Panel Fixed" in content:
        print("Panel already patched.")
    else:
        content = content.replace('constructor(scene) {', 'constructor(scene) {\n        // Transcendent Panel Fixed', 1)
        # Ensure correct indentation for UI_CONFIG
        content = content.replace('SHOW_DURATION: 600,', 'SHOW_DURATION: 600,\n    BOKEH_RADIUS: 0.5,\n    BOKEH_AMOUNT: 1.0,\n    BOKEH_CONTRAST: 0,\n    BOKEH_TARGET_RADIUS: 10,', 1)
        with open(path, 'w') as f: f.write(content)

def patch_uiscene():
    path = 'src/scripts/scenes/UIScene.js'
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()

    if "// Transcendent UI Fixed" in content:
        print("UIScene already patched.")
    else:
        # We search for a more generic block if possible or the one we just made
        if 'let wipe = this.splashScreen.postFX.addWipe(0.1, 0, 1);' in content:
            content = robust_sub(
                r'let wipe = this\.splashScreen\.postFX\.addWipe\(0\.1, 0, 1\); // wipeWidth, direction, axis',
                '// Transcendent UI Fixed\n            let wipe = this.splashScreen.postFX.addWipe(0.1, 1, 0); // wipeWidth, direction, axis',
                content, count=1
            )
            content = robust_sub(
                r'if \(this\.splashScreen\.postFX\) this\.splashScreen\.postFX\.remove\(wipe\);',
                'if (this.splashScreen.postFX) this.splashScreen.postFX.clear();',
                content, count=1
            )
            with open(path, 'w') as f: f.write(content)
        else:
             print("UIScene: Could not find target wipe block. Might already be patched or significantly different.")

if __name__ == "__main__":
    patch_main_scene()
    patch_panel()
    patch_uiscene()
    print("Robust patching orchestration complete.")
