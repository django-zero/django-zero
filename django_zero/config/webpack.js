var path = require("path");
var webpack = require("webpack");

const zeroPath = process.env.DJANGO_ZERO_BASE_DIR;
const ZERO_DIR = zeroPath;
const basePath = process.env.DJANGO_BASE_DIR;
const BASE_DIR = basePath;
const NODE_ENV = process.env.NODE_ENV || "production";
const WEBPACK_DEV_SERVER = process.env.WEBPACK_DEV_SERVER || false;

console.log("[ django-zero / webpack ] ZERO_DIR =", ZERO_DIR);
console.log("[ django-zero / webpack ] BASE_DIR =", BASE_DIR);
console.log("[ django-zero / webpack ] NODE_ENV =", NODE_ENV);
if (WEBPACK_DEV_SERVER) {
  console.log(
    "[ django-zero / webpack ] WEBPACK_DEV_SERVER =",
    WEBPACK_DEV_SERVER
  );
}

const resolveConfig = {
  alias: {},
  modules: [
    path.resolve(zeroPath, "node_modules"),
    path.resolve(basePath, "node_modules")
  ]
};

function createEntry() {
  if (WEBPACK_DEV_SERVER === "hot") {
    return ["webpack/hot/dev-server", ...arguments];
  } else if (WEBPACK_DEV_SERVER === "hot-only") {
    return ["webpack/hot/only-dev-server", ...arguments];
  } else if (WEBPACK_DEV_SERVER) {
    throw new Error("Invalid WEBPACK_DEV_SERVER value.");
  }
  return [...arguments];
}

function createWebpackConfig(
  withExamples = false,
  production = NODE_ENV === "production"
) {
  const MiniCssExtractPlugin = require("mini-css-extract-plugin");
  const AssetsPlugin = require("assets-webpack-plugin");

  let entries = {
    account: createEntry(path.resolve(zeroPath, "resources/assets/account.js")),
    bootstrap: createEntry(
      path.resolve(zeroPath, "resources/assets/bootstrap.js")
    )
  };

  if (withExamples) {
    entries = {
      ...entries,
      demo: path.resolve(zeroPath, "resources/assets/examples/demo.js")
    };
  }

  let cssLoaderOptions = { minimize: production };
  let styleLoader = [MiniCssExtractPlugin.loader];
  if (WEBPACK_DEV_SERVER) {
    styleLoader = ["style-loader"];
  }
  let stylePlugins = [
    new MiniCssExtractPlugin({
      filename: production ? "[name].[hash].css" : "[name].css",
      chunkFilename: production ? "[id].[hash].css" : "[id].css"
    })
  ];
  if (WEBPACK_DEV_SERVER) {
    stylePlugins = [];
  }

  let config = {
    context: basePath,
    target: "web",
    devtool: false,
    mode: production ? "production" : "development",

    resolve: resolveConfig,
    resolveLoader: resolveConfig,

    entry: entries,

    output: {
      path: path.resolve(basePath, ".cache/webpack"),
      publicPath: "/static/",
      filename: production ? "[name].[hash].js" : "[name].js",
      chunkFilename: production ? "[id].[hash].js" : "[id].js"
    },

    plugins: [
      ...stylePlugins,
      new AssetsPlugin({
        path: basePath,
        filename: "assets.json"
      }),
      new webpack.DefinePlugin({
        "process.env.NODE_ENV": JSON.stringify(NODE_ENV)
      }),
      new webpack.SourceMapDevToolPlugin({
        filename: "[file].map"
      })
    ],

    module: {
      rules: [
        {
          test: /\.(sc|sa|c)ss$/,
          use: [
            ...styleLoader,
            {
              loader: "css-loader"
            },
            {
              loader: "postcss-loader", // Run post css actions
              options: {
                plugins: function() {
                  return [require("autoprefixer")];
                }
              }
            },
            {
              loader: "resolve-url-loader"
            },
            {
              loader: "sass-loader?sourceMap"
            }
          ]
        },
        {
          test: /\.jsx?$/,
          use: ["babel-loader"]
        },
        {
          test: /\.(jpe?g|png|svg|ttf|woff|eot)$/,
          use: ["file-loader"]
        }
      ]
    },

    /*optimization: {
            splitChunks: {
                // include all types of chunks
                chunks: 'all'
            }
        },*/

    performance: {
      hints: "warning"
    }
  };

  if (WEBPACK_DEV_SERVER) {
    config.output.publicPath = "http://localhost:7999/static/";

    config.devServer = {
      hot: true,
      hotOnly: true,
      port: 7999,
      headers: { "Access-Control-Allow-Origin": "*" }
    };

    config.plugins.push(new webpack.HotModuleReplacementPlugin());
  }

  return config;
}

module.exports = {
  BASE_DIR,
  NODE_ENV,
  WEBPACK_DEV_SERVER,
  ZERO_DIR,
  basePath,
  createEntry,
  createWebpackConfig,
  zeroPath
};
