const BundleTracker = require("webpack-bundle-tracker");
const path = require("path");
const pages = {
  person: {
    entry: "./src/person.js",
    chunks: ["chunk-vendors"],
  },
};

module.exports = {
  pages: pages,
  filenameHashing: false,
  productionSourceMap: false,
  publicPath:
    process.env.NODE_ENV === "production" ? "" : "http://localhost:8080/",
  outputDir: path.resolve(__dirname, "dist"),

  chainWebpack: (config) => {
    config.module
      .rule("i18n")
      .resourceQuery(/blockType=i18n/)
      .type("javascript/auto")
      .use("i18n")
      .loader("@intlify/vue-i18n-loader");

    config.optimization.splitChunks({
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: "chunk-vendors",
          chunks: "all",
          priority: 1,
        },
      },
    });

    Object.keys(pages).forEach((page) => {
      config.plugins.delete(`html-${page}`);
      config.plugins.delete(`preload-${page}`);
      config.plugins.delete(`prefetch-${page}`);
    });

    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "../client/webpack-stats.json" }]);

    config.resolve.alias.set("__STATIC__", "static");
    // config.resolve.alias.set("vue", "vue/dist/vue.esm-bundler.js");

    config.devServer
      .public("http://localhost:8080")
      .host("localhost")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .writeToDisk(true)
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },
};
