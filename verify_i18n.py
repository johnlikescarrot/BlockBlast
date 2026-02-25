from playwright.sync_api import sync_playwright, Error as PlaywrightError
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
        page.wait_for_timeout(5000) # Give extra time for assets

        # 1. Assertion: Check page title
        assert "BlockBlast" in page.title(), f"Title mismatch: {page.title()}"
        print("Page title verified.")

        # 2. Check default localStorage (should be en or None)
        lang = page.evaluate("localStorage.getItem('blockblast_language')")
        print(f"Initial language in localStorage: {lang}")

        # Click Play button (Center)
        print("Starting game...")
        page.mouse.click(540, 540)
        page.wait_for_timeout(2000)

        # Verify page title again
        assert "BlockBlast" in page.title()

        print("Verification complete (Title asserted).")
        browser.close()

if __name__ == "__main__":
    try:
        run()
    except (PlaywrightError, AssertionError) as e:
        print(f"Verification failed: {e}")
        sys.exit(1) # Fail CI on assertion/playwright errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
