var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');

var app = express();

const fs = require('fs');

const csvSync = require('csv-parse/lib/sync');

const DB_FILE_PATH = JSON.parse(fs.readFileSync('./dbPath.json','utf8'));

const DB_INFO = JSON.parse(fs.readFileSync(DB_FILE_PATH.filePath,'utf8'));

// view engine setup

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);

var mysql = require('mysql2')

var con = mysql.createConnection({
  host: DB_INFO.host,
  user: DB_INFO.user,
  password: DB_INFO.password,
  database: DB_INFO.database,
  insecureAuth: DB_INFO.insecureAuth
});

app.get('/test', (req, res) => {
    res.send(sendData());
});

function sendData(){
  const file = 'data.csv';
  var data = fs.readFileSync(file);

  var res = {'data': csvSync(data)};
  var json = JSON.stringify(res);

  return json;
}

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
