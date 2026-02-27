const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
    console.log('Navigating to http://localhost:8080...');
    // Use domcontentloaded for faster initial navigation
    await page.goto('http://localhost:8080', { waitUntil: 'domcontentloaded' });

    // Deterministic wait for Phaser canvas
    console.log('Waiting for Phaser canvas to be visible...');
    await page.waitForSelector('canvas', { state: 'visible', timeout: 30000 });

    // Give a tiny bit of time for initial frame to render
    await page.waitForTimeout(1000);

    await page.screenshot({ path: 'final_verification.png' });
    console.log('Screenshot saved to final_verification.png');

    const title = await page.title();
    console.log('Page title:', title);

    const hasError = await page.evaluate(() => {
        return !!document.querySelector('.webpack-dev-server-client-overlay');
    });

    if (hasError) {
        console.error('Error: Webpack Error Overlay is present on the page.');
        process.exitCode = 1;
        throw new Error('Webpack Error Overlay detected');
    } else {
        console.log('Verification successful: No Webpack Error Overlay found.');
    }
  } catch (err) {
    console.error('Error during verification:', err);
    process.exitCode = 1;
    // Ensure we throw so the async wrapper/start-server-and-test catches the failure
    if (!process.exitCode) process.exitCode = 1;
  } finally {
    await browser.close();
  }
})();
