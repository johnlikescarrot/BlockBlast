from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8080')
        time.sleep(10) # Wait for Phaser and assets

        # Take screenshot of boot screen
        page.screenshot(path='final_boot_screen.png')
        print("Captured final_boot_screen.png")

        # Click Play (if visible) - we might need to click the canvas or a specific coord
        # In our case, the play button is at dim/2, dim/2. Dim is 1080.
        # So at 540, 540.
        page.mouse.click(540, 540)
        time.sleep(5)

        # Open options (in MenuScene or MainScene)
        # In MenuScene, the options button is also in the panel?
        # Actually, let's just wait and see what's on screen.

        # We can try to click where the Options button usually is.
        # In MainScene it's at 1010, 73 (pause) and 910, 73 (reload).
        # Let's try to trigger the options panel directly if possible, or just take more screenshots.

        page.screenshot(path='final_game_screen.png')
        print("Captured final_game_screen.png")

        browser.close()

if __name__ == "__main__":
    run()
