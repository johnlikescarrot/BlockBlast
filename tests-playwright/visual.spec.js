const { test, expect } = require('@playwright/test');
test('visual smoke test', async ({ page }) => {
  test.setTimeout(60000);
  await page.goto('/');
  await page.waitForFunction(() => window.Parchados && window.Parchados.game, { timeout: 30000 });

  await expect(page.locator('canvas')).toBeVisible();

  const viewport = page.viewportSize() ?? { width: 1080, height: 1080 };
  const { width, height } = viewport;

  await page.mouse.click(width / 2, height / 2);
  await page.waitForTimeout(5000); // Allow time for transitions
  await page.screenshot({ path: 'verification/beast_menu.png' });
});
