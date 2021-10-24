const path = require('path')
const webpack = require('webpack')
const createThemeColorReplacerPlugin = require('./config/plugin.config')
const CompressionWebpackPlugin = require('compression-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
const productionGzipExtensions = /\.(js|css|json|txt|html|ico|svg)(\?.*)?$/i;
const themeColor = require('./src/config/themeColor')

function resolve(dir) {
    return path.join(__dirname, dir)
}

const isProd = process.env.NODE_ENV === 'production'

// vue.config.js
const vueConfig = {
    publicPath: isProd ? "./static/" : '/',
    configureWebpack: config => {
        if (isProd) {
            return {
                plugins: [
                    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
                    new CompressionWebpackPlugin({
                        algorithm: 'gzip',
                        test: productionGzipExtensions,
                        threshold: 20480, //大于10kb压缩
                        minRatio: 0.8
                    }),
                    // new BundleAnalyzerPlugin() //打包分析插件 发布时请删除
                ]
            }
        } else {
            return {
                plugins: [
                    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
                    createThemeColorReplacerPlugin()
                ]
            }
        }
    },

    chainWebpack: (config) => {
        config.resolve.alias
            .set('@', resolve('src'))
            .set('./BaseMenu', path.resolve(__dirname, 'src/components/_util/BaseMenu.js'))

        const svgRule = config.module.rule('svg')
        svgRule.uses.clear()
        svgRule
            .oneOf('inline')
            .resourceQuery(/inline/)
            .use('vue-svg-icon-loader')
            .loader('vue-svg-icon-loader')
            .end()
            .end()
            .oneOf('external')
            .use('file-loader')
            .loader('file-loader')
            .options({
                name: 'assets/[name].[hash:8].[ext]'
            })
    },

    css: {
        loaderOptions: {
            less: {
                modifyVars: themeColor,
                javascriptEnabled: true
            }
        }
    },

    devServer: {
        port: 8000,
        hot: true,
        open: true,
		https:false
    },
    lintOnSave: false,
    // disable source map in production
    productionSourceMap: false,
    // babel-loader no-ignore node_modules/*
    transpileDependencies: [],
    runtimeCompiler: true, //启用运行的时的编译版本

}

if (process.env.VUE_APP_PREVIEW === 'true') {
    console.log('VUE_APP_PREVIEW', true)
}

module.exports = vueConfig