from playwright.sync_api import sync_playwright, Error as PlaywrightError
import sys
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 1080, 'height': 1080})
        page = context.new_page()

        if not os.path.exists('verification'):
            os.makedirs('verification')

        print("Navigating to game...")
        page.goto('http://localhost:8080', wait_until="networkidle")

        # Wait for the phaser canvas
        page.wait_for_selector("canvas", timeout=30000)
        page.wait_for_timeout(5000) # Wait for BootScene loading

        # 1. Click BootScene Play Button (Center)
        print("Clicking BootScene Play button...")
        page.mouse.click(540, 540)

        # Wait for Splash Screen (approx 3.5s) and Menu transition
        print("Waiting for splash screen and menu...")
        page.wait_for_timeout(5000)
        page.screenshot(path='verification/menu.png')

        # 2. Click Menu Play Button (Center-ish bottom)
        # startButton is at dim/2, dim/2+350 -> 540, 890
        print("Clicking Menu Start button...")
        page.mouse.click(540, 890)

        # Wait for loading slider in MenuScene (1.5s) and MainScene create
        print("Waiting for gameplay to load...")
        page.wait_for_timeout(3000)
        page.screenshot(path='verification/gameplay.png')

        # 3. Open Options from Gameplay (In-game settings button at 910, 73)
        # Wait, settings button in MainScene is at 910, 73
        print("Opening Options from Gameplay...")
        page.mouse.click(910, 73)
        page.wait_for_timeout(1000)
        page.screenshot(path='verification/options.png')

        # Assertion: Check page title
        assert "BlockBlast" in page.title(), f"Title mismatch: {page.title()}"
        print("Verification complete. Screenshots saved in /verification.")
        browser.close()

if __name__ == "__main__":
    try:
        run()
    except (PlaywrightError, AssertionError) as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
