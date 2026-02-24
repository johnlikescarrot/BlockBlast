const { merge } = require('webpack-merge');
const TerserPlugin = require('terser-webpack-plugin');
const JavaScriptObfuscator = require('webpack-obfuscator');
const path = require('path');
const base = require('./base');

module.exports = merge(base, {
  mode: 'production',
  output: {
    path: path.resolve(__dirname, '../dist'),
    filename: 'bundle.min.js',
  },
  devtool: false,
  performance: {
    maxEntrypointSize: 900000,
    maxAssetSize: 900000,
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          output: {
            comments: false,
          },
        },
      }),
    ],
  },
  plugins: [
    new JavaScriptObfuscator({
      compact: true,
      stringArray: true,
      stringArrayEncoding: ['base64'],
      stringArrayThreshold: 0.75,
      disableConsoleOutput: true,
      selfDefending: true,
    }),
  ],
});
