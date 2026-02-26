import sys

# Fix Panel.js
with open('src/scripts/components/panel.js', 'r') as f:
    panel = f.read()

panel = panel.replace("'Elastic.easeOut',\\n            easeParams: [1.2, 0.6]", "'Elastic.easeOut',\\n            easeParams: [1.2, 0.6]")
# Wait, the log says it has a literal \\n
panel = panel.replace("'Elastic.easeOut',\\n            easeParams: [1.2, 0.6]", "'Elastic.easeOut',\\n            easeParams: [1.2, 0.6]")
# Let's just rewrite the animateShow block
import re
panel = re.sub(r'animateShow\(container\) \{.*?\}',
'''animateShow(container) {
        container.setVisible(true);
        container.setScale(0.8);
        this.scene.tweens.add({
            targets: container,
            scale: 1,
            duration: 800,
            ease: 'Elastic.easeOut',
            easeParams: [1.2, 0.6]
        });
    }''', panel, flags=re.DOTALL)

with open('src/scripts/components/panel.js', 'w') as f:
    f.write(panel)

# Fix MainScene.js
with open('src/scripts/scenes/MainScene.js', 'r') as f:
    main = f.read()

# The log says: ERROR in ./src/scripts/scenes/MainScene.js: Missing semicolon. (570:19)
# and shows a closed bracket before BreakLine
# It looks like there's an extra } before BreakLine or a missing one inside ShowContainerWithFade

main = re.sub(r'ShowContainerWithFade\(scene, fila, columna, fadeInDuration, displayDuration, fadeOutDuration, container\) \{.*?\}\s+\}',
'''ShowContainerWithFade(scene, fila, columna, fadeInDuration, displayDuration, fadeOutDuration, container) {

        container.x = (fila*this.LAYOUT.SQUARE_SIZE )+this.LAYOUT.OFFSET_X
        container.y =(columna*this.LAYOUT.SQUARE_SIZE )+this.LAYOUT.OFFSET_Y
        // Crear el tween para el fade in
        scene.tweens.add({
            targets: container,
            alpha: 1, // Opacidad completa
            duration: fadeInDuration,
            onComplete: () => {
                // Después del fade in, esperar el displayDuration y luego hacer fade out
                scene.time.delayedCall(displayDuration, () => {
                    scene.tweens.add({
                        targets: container,
                        alpha: 0, // Volver a transparente
                        duration: fadeOutDuration,
                        onComplete: () => {
                            // Destruir el contenedor después del fade out
                            container.destroy();
                        }
                    });
                });
            }
        });
    }''', main, flags=re.DOTALL)

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.write(main)

print("Final Fix Applied")
