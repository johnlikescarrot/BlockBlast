from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Set viewport to match game dimensions to ensure coordinates work
        context = browser.new_context(viewport={'width': 1080, 'height': 1080})
        page = context.new_page()

        print("Navigating to game...")
        page.goto('http://localhost:8080')

        # Use proper waiting
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(5000) # Give Phaser some extra time to init

        # Assertion: Check page title
        title = page.title()
        print(f"Page Title: {title}")
        assert "BlockBlast" in title, f"Expected title to contain 'BlockBlast', but got '{title}'"

        # Take screenshot of boot screen
        page.screenshot(path='verify_boot.png')
        print("Captured verify_boot.png")

        # Click Play button (Center of the 1080x1080 canvas)
        print("Clicking Play button...")
        page.mouse.click(540, 540)

        # Wait for transition/splash
        page.wait_for_timeout(5000)

        # Capture Menu screen
        page.screenshot(path='verify_menu.png')
        print("Captured verify_menu.png")

        browser.close()
        print("Verification successful!")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
