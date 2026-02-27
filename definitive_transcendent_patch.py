import os
import re
import sys
import subprocess
import shutil

def robust_sub(pattern, replacement, content, count=0, *, literal=False):
    if literal:
        pattern = re.escape(pattern)
    new_content, n = re.subn(pattern, replacement, content, count=count)
    if n == 0:
        print(f"WARNING: Pattern not matched: {pattern!r:.80}")
    return new_content, n

def verify_js(path):
    node_bin = shutil.which("node")
    if not node_bin:
        print("ERROR: node binary not found in PATH")
        sys.exit(1)

    try:
        subprocess.run([node_bin, '--check', path], check=True, capture_output=True, text=True)
        print(f"Verified syntax for {path}")
    except subprocess.CalledProcessError as e:
        print(f"SYNTAX ERROR in {path}:")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: Could not execute {node_bin}")
        sys.exit(1)

def patch_main_scene():
    path = 'src/scripts/scenes/MainScene.js'
    if not os.path.exists(path):
        return False
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    # Authoritative Scoping fix
    if "// Transcendent Fixed Scoping" not in content:
        content, n = robust_sub(
            r'BreakLine\(x, y\) \{([\s\S]*?)let comboCount = this\.linesToClear\.length;',
            'BreakLine(x, y) {\n        // Transcendent Fixed Scoping\n        if (this.linesToClear.length < 1 || this.gamefinish) {\n            this.cameras.main.setZoom(1);\n            this.FinishTurn();\n            return;\n        }\n        let comboCount = this.linesToClear.length;',
            content, count=1
        )
        if n > 0:
            changed = True

    # Scoped shakeIntensity check
    if 'let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;' in content:
        match = re.search(r'if \(this\.animationsIterator === 0\) \{\s+let shakeIntensity', content)
        if not match:
            content, n = robust_sub(
                r'let shakeIntensity = comboCount \* JUICE_CONFIG\.SHAKE_INTENSITY_PER_LINE \* 1\.5;\s+if \(this\.animationsIterator === 0\) \{',
                'if (this.animationsIterator === 0) {\n            let shakeIntensity = comboCount * JUICE_CONFIG.SHAKE_INTENSITY_PER_LINE * 1.5;',
                content, count=1
            )
            if n > 0:
                changed = True

    # Shutdown cleanup for vignette/barrel - Authoritative Remove API fix
    # We replace the previous incorrect .remove() with the correct Phaser API
    if "this.cameras.main.postFX.remove(this.vignette)" not in content:
        # First, try to match the unpatched shutdown block if it exists
        unpatched_shutdown = r'this\.events\.once\(\'shutdown\', \(\) => \{ this\.cameras\.main\.setZoom\(1\); \}\);'
        incorrectly_patched_shutdown = r'this\.events\.once\(\'shutdown\', \(\) => \{\s+this\.vignette\?\.setActive\(false\);\s+this\.vignette\?\.remove\(\);'

        if re.search(incorrectly_patched_shutdown, content):
             content, n = robust_sub(
                incorrectly_patched_shutdown,
                "this.events.once('shutdown', () => {\n            this.vignette?.setActive(false);\n            if (this.vignette) this.cameras.main.postFX.remove(this.vignette);",
                content, count=1
            )
             if n > 0:
                 changed = True
                 # Also fix the barrel remove in the same block
                 content, n = robust_sub(
                     r'this\.barrel\?\.remove\(\);',
                     'if (this.barrel) this.cameras.main.postFX.remove(this.barrel);',
                     content, count=1
                 )
        elif re.search(unpatched_shutdown, content):
            content, n = robust_sub(
                unpatched_shutdown,
                "this.events.once('shutdown', () => {\n            this.vignette?.setActive(false);\n            if (this.vignette) this.cameras.main.postFX.remove(this.vignette);\n            this.barrel?.setActive(false);\n            if (this.barrel) this.cameras.main.postFX.remove(this.barrel);\n            this.vignette = null;\n            this.barrel = null;\n            this.cameras.main.setZoom(1);\n        });",
                content, count=1
            )
            if n > 0:
                changed = True

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
        return True
    return "// Transcendent Fixed Scoping" in content

def patch_panel():
    path = 'src/scripts/components/panel.js'
    if not os.path.exists(path):
        return False
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    if "// Transcendent Panel Fixed" not in content:
        content, n = robust_sub(
            'constructor(scene) {',
            'constructor(scene) {\n        // Transcendent Panel Fixed',
            content, literal=True, count=1
        )
        if n > 0:
            changed = True

    if "BOKEH_RADIUS" not in content:
        content, n = robust_sub(
            'SHOW_DURATION: 600,',
            'SHOW_DURATION: 600,\n    BOKEH_RADIUS: 0.5,\n    BOKEH_AMOUNT: 1.0,\n    BOKEH_CONTRAST: 0,\n    BOKEH_TARGET_RADIUS: 10,',
            content, literal=True, count=1
        )
        if n > 0:
            changed = True

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
        return True
    return "// Transcendent Panel Fixed" in content

def patch_uiscene():
    path = 'src/scripts/scenes/UIScene.js'
    if not os.path.exists(path):
        return False
    with open(path, 'r') as f:
        content = f.read()

    changed = False

    if "// Transcendent UI Fixed" not in content:
        # Full authoritative rewrite of splashScreenAnim to fix all bugs at once
        # including the alpha flash and redundant setVisible.
        pattern = r'    splashScreenAnim\(\)\{[\s\S]*?    setCurrentScene\(scene\)\{'
        replacement = """    splashScreenAnim(){
        this.graphics.setVisible(true);
        this.splashScreen.setAlpha(1);
        if (this.splashScreen.postFX) {
            // Transcendent UI Fixed
            let wipe = this.splashScreen.postFX?.addWipe?.(0.1, 1, 0);
            if (wipe) {
                this.tweens.add({
                    targets: wipe,
                    progress: 1,
                    duration: 1000,
                    ease: "Quint.easeOut",
                    onComplete: () => {
                        this.time.delayedCall(UI_CONFIG.SPLASH_DELAY, () => {
                            this.tweens.add({
                                targets: wipe,
                                progress: 0,
                                duration: 800,
                                ease: "Quint.easeIn",
                                onComplete: () => {
                                    if (this.splashScreen.postFX) this.splashScreen.postFX.clear();
                                    this.graphics.setVisible(false);
                                    this.splashScreen.setVisible(false);
                                }
                            });
                        });
                    }
                });
            } else {
                // Fallback if wipe creation failed
                this.time.delayedCall(UI_CONFIG.SPLASH_DELAY + 1000, () => {
                    this.graphics.setVisible(false);
                    this.splashScreen.setVisible(false);
                });
            }
        } else {
            this.splashScreen.setAlpha(0); // Fix visual flash
            let splashTween = this.tweens.add({
                targets: this.splashScreen,
                ease: 'sine.inout',
                duration: UI_CONFIG.SPLASH_FADE_DURATION,
                repeat: 0,
                alpha: {
                  getStart: () => 0,
                  getEnd: () => 1
                },
                onComplete: () => {
                    let splashTween2 = this.tweens.add({
                        targets: this.splashScreen,
                        ease: 'sine.inout',
                        duration: UI_CONFIG.SPLASH_FADE_DURATION,
                        repeat: 0,
                        delay: UI_CONFIG.SPLASH_DELAY,
                        alpha: {
                          getStart: () => 1,
                          getEnd: () => 0
                        },
                        onComplete: () => {
                            this.graphics.setVisible(false);
                            this.splashScreen.setVisible(false);
                            splashTween2?.remove();
                            splashTween2 = null;
                        }
                    });
                    splashTween?.remove();
                    splashTween = null;
                }
            });
        }
    }\n\n    setCurrentScene(scene){"""

        new_content, n = re.subn(pattern, replacement.replace('\\', '\\\\'), content, count=1)
        if n > 0:
            content = new_content
            changed = True
        else:
            print("WARNING: Authoritative UIScene patch failed to match.")

    if changed:
        with open(path, 'w') as f:
            f.write(content)
        verify_js(path)
        return True
    return "// Transcendent UI Fixed" in content

if __name__ == "__main__":
    s1 = patch_main_scene()
    s2 = patch_panel()
    s3 = patch_uiscene()

    if all([s1, s2, s3]):
        print("Transcendent patching orchestration complete.")
    else:
        print("CRITICAL: One or more patches failed or returned authoritative False.")
        sys.exit(1)
