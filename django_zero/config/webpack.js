var path = require('path');

const zeroPath = process.env.DJANGO_ZERO_BASE_DIR;
const basePath = process.env.DJANGO_BASE_DIR;
const resolveConfig = {
    modules: [
        path.resolve(zeroPath, 'node_modules'),
        path.resolve(basePath, 'node_modules'),
    ]
}

function createWebpackConfig(withExamples = false) {
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

    return {
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
            })
        ],

        module: {
            loaders: [
                {
                    test: /\.(scss)$/,
                    use: ExtractTextPlugin.extract({
                        fallback: 'style-loader',
                        use: [{
                            loader: 'css-loader',
                        }, {
                            loader: 'postcss-loader',
                            options: {
                                plugins: function () {
                                    return [
                                        require('precss'),
                                        require('autoprefixer')
                                    ];
                                }
                            }
                        }, {
                            loader: 'sass-loader'
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
                    test: /\.(jpg|png)$/, loader: 'url?limit=25000'
                },
                {
                    test: /\.svg$/, loader: 'file-loader'
                }
            ]
        },

        performance: {
            hints: "warning"
        },
    }
}

module.exports = {
    basePath,
    createWebpackConfig,
    zeroPath,
};
