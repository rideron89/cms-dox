const ExtractTextPlugin = require('extract-text-webpack-plugin')
const path              = require('path')
const webpack           = require('webpack')

var config = {
    entry: './src/index.js',

    output: {
        path: path.resolve(__dirname, 'public'),
        filename: 'bundle.js'
    },

    module: {
        rules: [
            { test: /\.vue$/, loader: 'vue-loader', options: {
                extractCSS: true
            } },

            { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ }
        ]
    },

    plugins: [
        new ExtractTextPlugin('style.css')
    ],

    performance: {
        hints: false
    },

    devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
    config.devtool = '#source-map'

    config.plugins = (config.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),

        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),

        new webpack.LoaderOptionsPlugin({
            minimize: true
        })
    ])
}

module.exports = config
