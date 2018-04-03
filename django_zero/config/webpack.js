var path = require('path');
var webpack = require('webpack');

const zeroPath = process.env.DJANGO_ZERO_BASE_DIR;
const basePath = process.env.DJANGO_BASE_DIR;
const NODE_ENV = process.env.NODE_ENV || 'production';

const resolveConfig = {
    modules: [
        path.resolve(zeroPath, 'node_modules'),
        path.resolve(basePath, 'node_modules'),
    ]
}

function createWebpackConfig(withExamples = false, production = (NODE_ENV == 'production')) {
    const ExtractTextPlugin = require('extract-text-webpack-plugin');
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

    let config = {
        context: basePath,
        devtool: 'eval-source-map',

        resolve: resolveConfig,
        resolveLoader: resolveConfig,

        entry: entries,

        output: {
            path: path.resolve(basePath, '.cache/webpack'),
            filename: '[name].js',
        },

        plugins: [
            new ExtractTextPlugin('[name].css'),
            new AssetsPlugin({
                path: basePath,
                filename: '.cache/assets.json',
            }),
            new webpack.DefinePlugin({
                'process.env': {
                    'NODE_ENV': JSON.stringify(NODE_ENV)
                }
            }),
        ],

        module: {
            loaders: [
                {
                    test: /\.css$/,
                    loaders: ['style-loader', 'css-loader', 'postcss-loader', 'resolve-url-loader']
                }, {
                    test: /\.scss$/,
                    use: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: [{
                            loader: 'css-loader',
                        }, {
                            loader: 'postcss-loader?sourceMap',
                            options: {
                                plugins: function () {
                                    return [
                                        require('precss'),
                                        require('autoprefixer')
                                    ];
                                },
                                sourceMap: true,
                            }
                        }, {
                            loader: 'resolve-url-loader',
                            options: { sourceMap: true }
                        }, {
                            loader: 'sass-loader?sourceMap'
                        }]
                    })
                },
                {
                    test: /\.jsx?$/,
                    use: {
                        loader: 'babel-loader',
                    }
                },
                {
                    test: /\.(jpe?g|png|svg|ttf|woff|eot)$/,
                    use: [{
                        loader: 'file-loader'
                    }]
                }
            ]
        },

        performance: {
            hints: "warning"
        },
    };

    if (production) {
        config.plugins.push(new webpack.optimize.UglifyJsPlugin())
    }

    return config;
}

module.exports = {
    NODE_ENV,
    basePath,
    createWebpackConfig,
    zeroPath,
};
