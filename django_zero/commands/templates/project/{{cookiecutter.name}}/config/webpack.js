const {createWebpackConfig} = require('django_zero/config/webpack');

let config = createWebpackConfig(withExamples=true);

// You can amend webpack configuration here.

module.exports = config;

