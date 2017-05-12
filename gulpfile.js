
/*
var native core modules
*/
var fs              = require('fs');
var http            = require('https')
var path            = require('path');

/*
var third-party deps
*/
var browserify      = require('browserify');
var babelify        = require('babelify'); // Used to convert ES6 & JSX to ES5
var through         = require('through2');
var path            = require('path');
var uuid            = require('node-uuid');

var gulp            = require('gulp');
var gulpBrowserify  = require('gulp-browserify');
var gulpif          = require('gulp-if');
var gutil           = require('gulp-util');
var less            = require('gulp-less');
var minifyCSS       = require('gulp-clean-css');
var rename          = require('gulp-rename');
var concat          = require('gulp-concat');
var order           = require('gulp-order');
var wrap            = require("gulp-wrap");
var watchify        = require('watchify');
var uglify          = require('gulp-uglify');
var sourcemaps      = require('gulp-sourcemaps');
var pug             = require('gulp-pug');
var S               = require('string');
var _               = require('lodash');
var source          = require('vinyl-source-stream');

/**
* Assembles a build object if we should add it
**/
var build_obj = null;

// is this for production ?
if (process.env.NODE_ENV === 'production') {

  // build up our current build information
  build_obj = {

    hash: uuid.v1().replace('-', '').substr(0, 10),
    year: new Date().getFullYear(),
    month: S(new Date().getMonth() + 1).padLeft(2, '0').s,
    day: new Date().getDate(),
    timestamp: new Date().getTime()

  };

  // write to file
  fs.writeFileSync('./build.json', JSON.stringify(build_obj));

}

var b =  null;
var createBundler = function(watch) {

  var w = browserify('./scripts/main.js', _.extend({}, watchify.args, {

    debug:        process.env.NODE_ENV !== 'production',
    delay:        10,
    ignoreWatch:  true,
    poll:         true

  })); 
  w.transform(babelify)

  // check watch
  if(watch === true) w = watchify(w)
  return w;

}

gulp.task('scripts', function() {

  // var callback = _.once(cb);
  var swallowError = function (error) {
    console.log(error);
    this.emit('end');
  }

  // check if we should shallow the error ?
  if(process.env.NODE_ENV === 'production') {

    // Build production with old gulp files
    return gulp.src('./scripts/main.js', { read: false })
    .pipe(gulpBrowserify({
      transform: ['babelify'],
      extensions: [],
      debug : false
    }))
    .pipe(uglify({}))
    .pipe(rename('app.' + build_obj.hash + '.min.js'))
    .pipe(gulp.dest('./public/js/'))

  } else {

    // create bundler
    if(!b) b = createBundler(false);

    // Build
    return b.bundle()
    .on('error', swallowError)
    .pipe(source('app.js'))
    .pipe(gulp.dest('./public/js/'))

  }

});

/**
*
**/
gulp.task('styles', function(cb) {

  // Build
  gulp.src([

    'styles/main.less'

  ])
  .pipe(less())
  .pipe(concat('app' + (build_obj ? '.' + build_obj.hash + '.min' : '') + '.css'))
  .pipe(gulpif(process.env.NODE_ENV !== 'production', sourcemaps.write('.')))
  .pipe(gulpif(process.env.NODE_ENV === 'production', minifyCSS({

    advanced: true,
    keepSpecialComments: false

  })))
  .pipe(gulp.dest('./public/css'))
  .on('end', cb);

});

/**
* Watch the gulp item
**/
gulp.task('watch', function(){

  if(!b) b = createBundler(false);

  // run the style setups
  gulp.watch([ 'styles/**/*.less', 'styles/*.less' ], [ 'styles' ]);
  gulp.watch([ 'scripts/**/*.js', 'scripts/*.js'], [ 'scripts' ]);
  gulp.watch([ 'templates/**/*.pug', 'templates/*.pug' ], [ 'templates' ]);

});

// does the complete build
gulp.task('build', [ 'styles', 'templates', 'scripts' ]);

// The default task (called when you run `gulp` = require(cli));
gulp.task('default', []);
