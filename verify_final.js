const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(5000); // Wait for Phaser to load
  await page.screenshot({ path: 'verification_final.png' });
  await browser.close();
})();
