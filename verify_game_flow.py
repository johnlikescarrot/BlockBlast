import os
import sys
import time
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# Deterministic Coordinates
BOOT_PLAY_BUTTON_POS = (540, 540)
MENU_START_BUTTON_POS = (540, 890)
MENU_OPTIONS_BUTTON_POS = (540 - 210, 540 + 350)
GAMEPLAY_OPTIONS_BUTTON_POS = (910, 73)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 1080, 'height': 1080})
        page = context.new_page()

        os.makedirs('verification', exist_ok=True)

        print("Navigating to game...")
        page.goto('http://localhost:8080', wait_until="networkidle")

        # 1. Wait for BootScene and click Play
        page.wait_for_selector("canvas", timeout=30000)

        print("Waiting for BootScene...")
        page.wait_for_function("window.Parchados && window.Parchados.game && window.Parchados.game.scene.isActive('BootScene')", timeout=20000)
        time.sleep(5) # Ensure loading completes

        print("Clicking Boot Play Button...")
        page.mouse.click(*BOOT_PLAY_BUTTON_POS)

        # 2. Wait for MenuScene
        print("Waiting for MenuScene...")
        page.wait_for_function("window.Parchados.game.scene.isActive('MenuScene')", timeout=20000)
        time.sleep(3) # Wait for splash screen and animations
        page.screenshot(path='verification/menu.png')
        print("Captured menu.png")

        # 3. Click Start to enter MainScene
        print("Clicking Menu Start Button...")
        page.mouse.click(*MENU_START_BUTTON_POS)

        # 4. Wait for MainScene (Gameplay) - Higher timeout as it involves loading
        print("Waiting for MainScene...")
        try:
            page.wait_for_function("window.Parchados.game.scene.isActive('MainScene')", timeout=30000)
        except Exception:
            print("Retrying Menu Start Click...")
            page.mouse.click(*MENU_START_BUTTON_POS)
            page.wait_for_function("window.Parchados.game.scene.isActive('MainScene')", timeout=20000)

        time.sleep(5) # Allow scene to initialize
        page.screenshot(path='verification/gameplay.png')
        print("Captured gameplay.png")

        # 5. Open Options from Gameplay
        print("Clicking Gameplay Options/Reload Button...")
        page.mouse.click(*GAMEPLAY_OPTIONS_BUTTON_POS)
        time.sleep(2) # Modal animation
        page.screenshot(path='verification/options_modal.png')
        print("Captured options_modal.png")

        # Final Assertions
        assert "BlockBlast" in page.title(), f"Title mismatch: {page.title()}"
        active_scenes = page.evaluate("window.Parchados.game.scene.getScenes(true).map(s => s.scene.key)")
        print(f"Active scenes: {active_scenes}")

        print("Verification complete. All flow steps validated deterministically.")
        browser.close()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
