const path = require('path');
const gulp = require('gulp');
const mainBowerFiles = require('main-bower-files');

const conf = require('./conf/gulp.conf');

gulp.task('fonts', function () {
      return gulp.src(mainBowerFiles('**/*.{otf,eot,svg,ttf,woff,woff2}'))
        .pipe(gulp.dest(path.join(conf.paths.dist, '/fonts/')))
        .pipe(gulp.dest(path.join(conf.paths.dist, '/webfonts/')));
});
