// karma.conf.js
var webpack = require('webpack');

module.exports = function (config) {
    config.set({
        browsers: ['Chrome', 'Firefox', 'IE', 'Safari'],
        customLaunchers: {
          IE9: {
            base: 'IE',
            'x-ua-compatible': 'IE=EmulateIE9'
          },
          IE8: {
            base: 'IE',
            'x-ua-compatible': 'IE=EmulateIE8'
          }
        },
        singleRun: true,
        frameworks: ['mocha'],
        files: [
            'tests.webpack.js'
        ],
        preprocessors: {
            'tests.webpack.js': ['webpack']
        },
        reporters: ['progress'],
        webpack: {
            module: {
                loaders: [
                    {test: /\.js?$/, exclude: /node_modules/, loader: 'babel-loader'}
                ]
            },
            externals: {
                  'cheerio': 'window',
                  'react/addons': true,
                  'react/lib/ExecutionEnvironment': true,
                  'react/lib/ReactContext': true
            },
            watch: true
        },
        webpackServer: {
            noInfo: true
        }
    });
};