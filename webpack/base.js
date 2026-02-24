const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin'); 
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const Dotenv = require('dotenv-webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = { 
   mode: 'production',
   output: {
      publicPath: 'auto',
      path: path.resolve(__dirname, '../dist'),
      filename: 'bundle.[contenthash].js'
   },
   devtool: 'source-map',
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
         },
         {
            test: /\.css$/i,
            use: [MiniCssExtractPlugin.loader, 'css-loader'],
         },
      ],
   },
   plugins: [
      new CleanWebpackPlugin(),
      new webpack.DefinePlugin({
         CANVAS_RENDERER: JSON.stringify(true),
         WEBGL_RENDERER: JSON.stringify(true),
      }),
      new HtmlWebpackPlugin({
         template: './index.html',
         minify: {
            removeComments: true,
            collapseWhitespace: true,
            removeRedundantAttributes: true,
            useShortDoctype: true,
            removeEmptyAttributes: true,
            removeStyleLinkTypeAttributes: true,
            keepClosingSlash: true,
            minifyJS: true,
            minifyCSS: true,
            minifyURLs: true,
         },
      }),
      new MiniCssExtractPlugin({
         filename: 'style.[contenthash].css'
      }),
      new Dotenv(),
   ],
}
