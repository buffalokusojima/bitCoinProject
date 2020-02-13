var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');

var app = express();

const fs = require('fs');

const csvSync = require('csv-parse/lib/sync');

const moment = require('moment');

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

const table = ["price_1min", "price_1hour"];

app.get('/test', (req, res) => {
  
  const term = req.query.term;
  var selectedTable;
  
  if(term == "min"){
      selectedTable = table[0];
  }else if(term == "hour"){
      selectedTable = table[1];
  }else{
      res.status(404).send("Error");
  }
  
  var sql = "SELECT * from " + selectedTable + " WHERE date BETWEEN '2019-09-29 00:00:01' AND '2019-09-30 00:00:00'";
  
  console.log(sql)
  con.query(sql, function(err, result){
      if(err){
        res.status(500).send("Error");
      }
      res.send(JSON.stringify({"data": result}))
    });
    
});

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
