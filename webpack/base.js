const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = {
  mode: 'development',
  devtool: 'eval-source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        include: path.resolve(__dirname, '../src/'),
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: [/\.vert$/, /\.frag$/],
        use: 'raw-loader',
      },
      {
        test: /\.(gif|png|jpe?g|svg|xml)$/i,
        use: 'file-loader',
      },
      {
        test: /\.(ogg|wav)$/i,
        use: 'file-loader',
      }
    ],
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({ patterns: [{ from: "src/scripts/locales", to: "scripts/locales" }, { from: "src/shaders", to: "shaders" }] }),
    new webpack.DefinePlugin({
      CANVAS_RENDERER: JSON.stringify(true),
      WEBGL_RENDERER: JSON.stringify(true),
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
      'process.env.ASSET_PATH': JSON.stringify(process.env.ASSET_PATH || ''),
    }),
    new HtmlWebpackPlugin({
      template: './index.html',
    }),
    new Dotenv(),
  ],
};
