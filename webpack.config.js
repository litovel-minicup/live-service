const path = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');


module.exports = {
    entry: {
        MatchOnline: ['./minicup_live_service/static/MatchOnline/main.js', 'bootstrap-loader'],
        MatchOverview: ['./minicup_live_service/static/MatchOverview/main.js', 'bootstrap-loader'],
        Exhibition: ['./minicup_live_service/static/Exhibition/main.js', 'bootstrap-loader'],
    },
    output: {
        path: path.resolve(__dirname, 'minicup_live_service/static/build/'),
        publicPath: '/static/build/',
        filename: '[name].build.js'
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ],
            }, {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {}
                    // other vue-loader options go here
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'postcss-loader', 'sass-loader'],

                // postcss: {},
            },

        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery",
            Tether: "tether",
            "window.Tether": "tether",
            Alert: "exports-loader?Alert!bootstrap/js/dist/alert",
            Button: "exports-loader?Button!bootstrap/js/dist/button",
            Carousel: "exports-loader?Carousel!bootstrap/js/dist/carousel",
            Collapse: "exports-loader?Collapse!bootstrap/js/dist/collapse",
            // Dropdown: "exports-loader?Dropdown!bootstrap/js/dist/dropdown",
            Modal: "exports-loader?Modal!bootstrap/js/dist/modal",
            // Popover: "exports-loader?Popover!bootstrap/js/dist/popover",
            Scrollspy: "exports-loader?Scrollspy!bootstrap/js/dist/scrollspy",
            Tab: "exports-loader?Tab!bootstrap/js/dist/tab",
            // Tooltip: "exports-loader?Tooltip!bootstrap/js/dist/tooltip",
            Util: "exports-loader?Util!bootstrap/js/dist/util",
        })
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },
    devServer: {
        historyApiFallback: true,
        noInfo: true,
        overlay: true,
        proxy: {
            '**': {
                target: 'http://localhost:8888',
                secure: false
            }
        }
    },
    performance: {
        hints: false
    },
    devtool: '#eval-source-map'
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map';
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new UglifyJSPlugin({
            sourceMap: true,
            /* minimize: true,
            compress: {
                warnings: false
            },
            output: {
                comments: false
            }*/
        }),
    ])
}
