const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    console.log('Navigating to http://localhost:8080...');
    await page.goto('http://localhost:8080', { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000); // Wait for Phaser to init
    await page.screenshot({ path: 'final_verification.png' });
    console.log('Screenshot saved to final_verification.png');
    const title = await page.title();
    console.log('Page title:', title);
    const hasError = await page.evaluate(() => {
        return !!document.querySelector('.webpack-dev-server-client-overlay');
    });
    console.log('Webpack Error Overlay present:', hasError);
  } catch (err) {
    console.error('Error during verification:', err);
  } finally {
    await browser.close();
  }
})();
