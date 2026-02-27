const { test, expect } = require('@playwright/test');
test('capture snapshots', async ({ page }) => {
  await page.goto('/');
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'verification/beast_loading.png' });

  // Click play if visible
  const playButton = page.locator('canvas');
  if (await playButton.isVisible()) {
    await page.mouse.click(540, 540); // Center click
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'verification/beast_menu.png' });

    await page.mouse.click(540, 900); // Start button area
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'verification/beast_gameplay.png' });
  }
});
