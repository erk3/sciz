const gulp = require('gulp');
const nginclude = require('gulp-nginclude');
const htmlmin = require('gulp-htmlmin');
const angularTemplatecache = require('gulp-angular-templatecache');

const conf = require('./conf/gulp.conf');

gulp.task('partials', partials);

function partials() {
  return gulp.src(conf.path.src('app/**/*.html'))
    .pipe(htmlmin(conf.htmlmin))
    .pipe(angularTemplatecache('templateCacheHtml.js', {
      module: conf.ngModule,
      root: 'app'
    }))
    .pipe(nginclude())
    .pipe(gulp.dest(conf.path.tmp()));
}