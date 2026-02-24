const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin'); 
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin'); 
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = { 
   mode: 'development',
   output: {
      publicPath: 'auto',
      path: path.resolve(__dirname, '../dist')
   },
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
            use: ['style-loader', 'css-loader'],
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
      }),
      new Dotenv(),
   ],
}
