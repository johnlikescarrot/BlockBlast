from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 1080, 'height': 1080})
        page = context.new_page()

        print("Navigating to game...")
        page.goto('http://localhost:8080', wait_until="networkidle")

        # Wait for the phaser canvas
        page.wait_for_selector("canvas", timeout=30000)

        # Assertion: Check page title
        assert "BlockBlast" in page.title()
        print("Page title verified.")

        # Take screenshots for manual verification
        page.screenshot(path='final_verify_boot.png')

        # Click Play button (Center)
        page.mouse.click(540, 540)
        page.wait_for_timeout(5000)
        page.screenshot(path='final_verify_menu.png')

        browser.close()
        print("Verification complete (Title asserted, screenshots saved).")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
