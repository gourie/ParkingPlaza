// tests.webpack.js
var context = require.context('./__test__', true, /-test\.js?$/);
context.keys().forEach(context);