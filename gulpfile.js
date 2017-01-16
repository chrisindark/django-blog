var gulp = require('gulp');
var uglify = require('gulp-uglify');

gulp.task('default', ['build'], function () {
});

gulp.task('build', function () {
    return gulp.src('static/javascripts/**/*.js')
        .pipe(ngAnnotate())
        .pipe(uglify())
        .pipe(gulp.dest('dist/static/javascripts/'));
});
