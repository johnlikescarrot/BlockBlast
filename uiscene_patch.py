import sys

def patch_uiscene():
    path = 'src/scripts/scenes/UIScene.js'
    with open(path, 'r') as f: content = f.read()

    # Cinematic Reveal Logic
    old_anim = """    splashScreenAnim(){
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
    }"""

    new_anim = """    splashScreenAnim(){
        this.graphics.setVisible(true);
        this.splashScreen.setAlpha(1);
        let wipe = this.splashScreen.postFX.addWipe(0, 1, 0); // direction, axis, reveal

        this.tweens.add({
            targets: wipe,
            progress: 1,
            duration: 1000,
            ease: 'Quint.easeOut',
            onComplete: () => {
                this.time.delayedCall(UI_CONFIG.SPLASH_DELAY, () => {
                    this.tweens.add({
                        targets: wipe,
                        progress: 0,
                        duration: 800,
                        ease: 'Quint.easeIn',
                        onComplete: () => {
                            this.graphics.setVisible(false);
                            this.splashScreen.setVisible(false);
                        }
                    });
                });
            }
        });
    }"""

    content = content.replace(old_anim, new_anim)
    with open(path, 'w') as f: f.write(content)

patch_uiscene()
