import re

path = 'src/scripts/scenes/UIScene.js'

robust_anim = """    splashScreenAnim(){
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
            this.graphics.setVisible(true);
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
    }"""

with open(path, 'r') as f:
    content = f.read()

# Match the entire splashScreenAnim method including corrupted trailing blocks
# Using a broad regex that looks for the start and continues until the next method or end of class
pattern = r'    splashScreenAnim\(\)\{[\s\S]*?    setCurrentScene\(scene\)\{'
replacement = robust_anim + "\n\n    setCurrentScene(scene){"

content = re.sub(pattern, replacement, content, count=1)

with open(path, 'w') as f:
    f.write(content)
