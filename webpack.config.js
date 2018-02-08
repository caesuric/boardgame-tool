var path = require('path')
const webpack = require('webpack')
var WebpackBuildNotifierPlugin = require('webpack-build-notifier')

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'web'),
        filename: 'js/index.js',
        sourcePrefix: ''
    },
    module: {
        loaders: [
            {
                test: /\.(css|scss)$/,
                loaders: [
                    'style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.html$/,
                loaders: [
                    'html-loader'
                ]
            },
            {
                test: /\.(eot|woff|woff2|svg|ttf|png|jpg)([\?]?.*)$/,
                loaders: [
                    'file-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env']
                    }
                }
            }
        ],
        unknownContextCritical: false
    },
    devtool: 'source-map',
    resolve: {
        alias: {
            jquery: 'jquery/src/jquery'
        },
        modules: [
            'node_modules',
            path.resolve(__dirname, 'src/lib'),
            path.resolve(__dirname, 'src/scss')
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        new WebpackBuildNotifierPlugin({})
    ]
}
