import os
import sys
import time
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# Deterministic Coordinates
BOOT_PLAY_BUTTON_POS = (540, 540)
MENU_START_BUTTON_POS = (540, 890)
GAMEPLAY_OPTIONS_BUTTON_POS = (910, 73)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            context = browser.new_context(viewport={'width': 1080, 'height': 1080})
            page = context.new_page()

            os.makedirs('verification', exist_ok=True)

            print("Navigating to game...")
            page.goto('http://localhost:8080', wait_until="networkidle")

            # 1. Wait for BootScene and click Play
            page.wait_for_selector("canvas", timeout=30000)

            print("Waiting for BootScene...")
            page.wait_for_function("window.Parchados && window.Parchados.game && window.Parchados.game.scene.isActive('BootScene')", timeout=20000)

            # Wait for loading to finish (the loading slider reaches 1.0)
            print("Waiting for loading to finish...")
            page.wait_for_function("window.Parchados.game.scene.getScene('BootScene').loadingSlider.value >= 0.99", timeout=15000)
            page.wait_for_timeout(2000) # Final button appearance delay

            print("Clicking Boot Play Button...")
            page.mouse.click(*BOOT_PLAY_BUTTON_POS)

            # 2. Wait for MenuScene
            print("Waiting for MenuScene...")
            page.wait_for_function("window.Parchados.game.scene.isActive('MenuScene')", timeout=10000)

            # Wait for splash screen fade out (verified via UIScene state if possible, or timeout)
            page.wait_for_timeout(3000)
            page.screenshot(path='verification/menu.png')
            print("Captured menu.png")

            # 3. Click Start to enter MainScene
            print("Clicking Menu Start Button...")
            page.mouse.click(*MENU_START_BUTTON_POS)

            # 4. Wait for MainScene (Gameplay)
            print("Waiting for MainScene...")
            # We retry the click if needed since transition can be async
            try:
                page.wait_for_function("window.Parchados.game.scene.isActive('MainScene')", timeout=20000)
            except Exception:
                print("Retrying Menu Start Click...")
                page.mouse.click(*MENU_START_BUTTON_POS)
                page.wait_for_function("window.Parchados.game.scene.isActive('MainScene')", timeout=10000)

            # Wait until gameplay logic is initialized
            page.wait_for_function("window.Parchados.game.scene.getScene('MainScene').startTime > 0", timeout=10000)
            page.wait_for_timeout(2000)
            page.screenshot(path='verification/gameplay.png')
            print("Captured gameplay.png")

            # 5. Open Options from Gameplay
            print("Clicking Gameplay Options/Reload Button...")
            page.mouse.click(*GAMEPLAY_OPTIONS_BUTTON_POS)

            # Wait for modal visibility
            page.wait_for_function("window.Parchados.game.scene.getScene('UIScene').panel.reloadContainer.visible", timeout=5000)
            page.wait_for_timeout(1000)
            page.screenshot(path='verification/options_modal.png')
            print("Captured options_modal.png")

            # Final Assertions
            assert "BlockBlast" in page.title(), f"Title mismatch: {page.title()}"
            print("Verification complete. All flow steps validated deterministically.")

        finally:
            print("Closing browser...")
            browser.close()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
