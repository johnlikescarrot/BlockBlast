const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests-playwright',
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
  },
});
