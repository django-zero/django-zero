var path = require('path');
var webpack = require('webpack');

const zeroPath = process.env.DJANGO_ZERO_BASE_DIR;
const basePath = process.env.DJANGO_BASE_DIR;
const NODE_ENV = process.env.NODE_ENV || 'production';

const resolveConfig = {
    alias: {},
    modules: [
        path.resolve(zeroPath, 'node_modules'),
        path.resolve(basePath, 'node_modules'),
    ]
}

function createWebpackConfig(withExamples = false, production = (NODE_ENV === 'production')) {
    const MiniCssExtractPlugin = require("mini-css-extract-plugin");
    const AssetsPlugin = require('assets-webpack-plugin');

    let entries = {
        account: path.resolve(zeroPath, 'resources/assets/account.js'),
        bootstrap: path.resolve(zeroPath, 'resources/assets/bootstrap.js'),
    };

    if (withExamples) {
        entries = {
            ...entries,
            'demo': path.resolve(zeroPath, 'resources/assets/examples/demo.js'),
        }
    }

    let cssLoaderOptions = {minimize: production};

    let config = {
        context: basePath,
        target: 'web',
        devtool: production ? false : 'eval-source-map',
        mode: production ? 'production' : 'development',

        resolve: resolveConfig,
        resolveLoader: resolveConfig,

        entry: entries,

        output: {
            path: path.resolve(basePath, '.cache/webpack'),
            filename: '[name].js',
        },

        plugins: [
            new MiniCssExtractPlugin({
                filename: '[name].css',
                chunkFilename: '[id].css',
            }),
            new AssetsPlugin({
                path: basePath,
                filename: 'assets.json',
            }),
            new webpack.DefinePlugin({
                'process.env': {
                    'NODE_ENV': JSON.stringify(NODE_ENV)
                }
            }),
        ],

        module: {
            rules: [
                {
                    test: /\.(sc|sa|c)ss$/,
                    use: [{
                        loader: MiniCssExtractPlugin.loader,
                    }, {
                        loader: 'css-loader',
                    }, {
                        loader: 'postcss-loader', // Run post css actions
                        options: {
                            plugins: function () {
                                return [
                                    require('autoprefixer')
                                ];
                            },
                        }
                    }, {
                        loader: 'resolve-url-loader'
                    }, {
                        loader: 'sass-loader?sourceMap'
                    }]
                },
                {
                    test: /\.jsx?$/,
                    use: [
                        'babel-loader',
                    ]
                },
                {
                    test: /\.(jpe?g|png|svg|ttf|woff|eot)$/,
                    use: [
                        'file-loader',
                    ]
                }
            ]
        },

        performance: {
            hints: "warning"
        },
    };

    return config;
}

module.exports = {
    NODE_ENV,
    basePath,
    createWebpackConfig,
    zeroPath,
};
