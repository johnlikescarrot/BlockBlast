const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests-playwright',
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    viewport: { width: 1080, height: 1080 },
  },
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
