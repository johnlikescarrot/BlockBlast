const { merge } = require('webpack-merge');
const TerserPlugin = require('terser-webpack-plugin');
const JavaScriptObfuscator = require('webpack-obfuscator');
const base = require('./base');

module.exports = merge(base, {
   mode: 'production',
   output: {    
      filename: 'bundle.[contenthash].min.js',
   },  
   devtool: false,
   performance: {    
      maxEntrypointSize: 2000000,
      maxAssetSize: 2000000,
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
