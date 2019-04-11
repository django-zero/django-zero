const path = require("path");
const {
  createWebpackConfig,
  createEntry,
  basePath
} = require("django_zero/config/webpack");

let config = createWebpackConfig((withExamples = true));

// You can amend webpack configuration here.
// config.entry = {
//   acme: createEntry(path.resolve(basePath, "apps/acme/resources/assets/acme.js"))
// }

module.exports = config;
