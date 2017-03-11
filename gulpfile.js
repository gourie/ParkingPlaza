/* File: gulpfile.js
*   author: Joeri Nicolaes
*   email: joerinicolaes@gmail.com
*/

var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var browserify = require('browserify');
var resolutions = require('browserify-resolutions');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var gutil = require('gulp-util');
var babelify = require('babelify');
var reactify = require('reactify');
var uglify = require('gulp-uglify');
var cssmin = require('gulp-minify-css');

// External dependencies you do not want to rebundle while developing,
// but include in your application deployment
var dependencies = [
	'react',
  	'react-dom'
];
// keep a count of the times a task refires
var scriptsCount = 0;

// Gulp tasks
// ----------------------------------------------------------------------------
gulp.task('scripts', ['css'], function () {
    bundleApp(false);
});

gulp.task('deploy', ['min-css'], function (){
	bundleApp(true);
});

gulp.task('copyreactdatepickerstyles', function() {
    return gulp.src('./node_modules/react-datepicker/dist/react-datepicker.min.css')
        .pipe(gulp.dest('./src'))
});

gulp.task('reactwidget', function() {
    return gulp.src('./node_modules/react-widgets/dist/css/react-widgets.css')
        .pipe(gulp.dest('./src'))
});

gulp.task('less', function () {
    return gulp.src('./src/*.less')
        .pipe(less())
        .pipe(gulp.dest('./src'))
});

gulp.task('css', ['less','copyreactdatepickerstyles','reactwidget'], function () {
    return gulp.src('./src/*.css')
        .pipe(concat('style.css'))
        .pipe(gulp.dest('./static'))
});

gulp.task('min-css', ['less','copyreactdatepickerstyles','reactwidget'], function () {
    return gulp.src('./src/*.css')
        .pipe(concat('style.min.css'))
        .pipe(cssmin())
        .pipe(gulp.dest('./static'))
});

gulp.task('watch', function () {
	gulp.watch(['./src/**/*.js'], ['scripts']);
	gulp.watch(['./src/*.css'], ['css']);
	gulp.watch(['./src/*.less'], ['less']);
});

// When running 'gulp' on the terminal this task will fire.
// It will start watching for changes in every .js file.
// If there's a change, the task 'scripts' defined above will fire.
gulp.task('default', ['scripts','watch']);

// Private Functions
// ----------------------------------------------------------------------------
function bundleApp(isProduction) {
	scriptsCount++;
	// Browserify will bundle all our js files together in to one and will let
	// us use modules in the front end.
	var mapAppBundler = browserify({
    	entries: './src/map.js',
    	debug: false
  	})

	var homeAppBundler = browserify({
    	entries: './src/home.js',
    	debug: false
  	})

	var tosAppBundler = browserify({
    	entries: './src/tos.js',
    	debug: false
  	})

	var calendarAppBundler = browserify({
    	entries: './src/CalendarApp.js',
    	debug: false
  	})

	var parkingListAppBundler = browserify({
    	entries: './src/ParkingListApp.js',
    	debug: false
  	})

	var indexAppBundler = browserify({
    	entries: './src/index.js',
    	debug: false
  	})

	var emailconfAppBundler = browserify({
    	entries: './src/emailconf.js',
    	debug: false
  	})

	// If it's not for production, a separate vendors.js file will be created
	// the first time gulp is run so that we don't have to rebundle things like
	// react everytime there's a change in the js file
  	if (!isProduction && scriptsCount === 1){
  		// create vendors.js for dev environment.
  		browserify({
			require: dependencies,
			debug: false
		})
			.bundle()
			.on('error', gutil.log)
			.pipe(source('vendors.js'))
			.pipe(gulp.dest('./static/'));
  	}
  	if (!isProduction){
  		// make the dependencies external so they dont get bundled by the
		// app bundler. Dependencies are already bundled in vendor.js for
		// development environments.
  		dependencies.forEach(function(dep){
  			mapAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			homeAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			tosAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			calendarAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			parkingListAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			indexAppBundler.external(dep);
  		})
  		dependencies.forEach(function(dep){
  			emailconfAppBundler.external(dep);
  		})
  	}

  	if (!isProduction) {
  	    mapAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('mapapp.js'))
            .pipe(gulp.dest('./static/'));
  	    homeAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('homeapp.js'))
            .pipe(gulp.dest('./static/'));
  	    tosAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('tosapp.js'))
            .pipe(gulp.dest('./static/'));
  	    calendarAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('calendarapp.js'))
            .pipe(gulp.dest('./static/'));
  	    parkingListAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('parkinglistapp.js'))
            .pipe(gulp.dest('./static/'));
  	    indexAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('indexapp.js'))
            .pipe(gulp.dest('./static/'));
        emailconfAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('emailconfapp.js'))
            .pipe(gulp.dest('./static/'));
    } else {
        //production build
        mapAppBundler
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('mapapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        homeAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('homeapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        tosAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('tosapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        calendarAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('calendarapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        parkingListAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('parkinglistapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        indexAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('indexapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
        emailconfAppBundler
            .plugin(resolutions, 'react')
            // transform ES6 and JSX to ES5 with babelify
            .transform("babelify", {presets: ["es2015", "react"]})
            .bundle()
            .on('error',gutil.log)
            .pipe(source('emailconfapp.min.js'))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(gulp.dest('./static/'));
    }
}
