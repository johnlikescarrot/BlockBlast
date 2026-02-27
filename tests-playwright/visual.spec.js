const { test, expect } = require('@playwright/test');
test('visual presence', async ({ page }) => {
  await page.goto('/');
  await page.waitForFunction(() => window.Parchados && window.Parchados.game);

  // Verify game canvas is visible
  const canvas = page.locator('canvas');
  await expect(canvas).toBeVisible();

  // Dim background or splash can be clicked
  const { width, height } = page.viewportSize();
  await page.mouse.click(width / 2, height / 2);

  // Wait for menu
  await page.waitForTimeout(2000);

  // Take a single screenshot for record (non-comparing)
  await page.screenshot({ path: 'verification/final_smoke_test.png' });
});
