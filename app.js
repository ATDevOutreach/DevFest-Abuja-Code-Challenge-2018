// Importing modules and routes
const express       = require('express'),
      bodyparser    = require('body-parser'),
      dotenv        = require('dotenv').config(),
      mongoose      = require('mongoose'),
      flash         = require('connect-flash'),
      session       = require('express-session'),
      sms           = require('./routes/sms'),
      call          = require('./routes/call'),
      landing       = require('./routes/landing');

// Connecting to mlab database
mongoose.connect(process.env.mlab_url,{useNewUrlParser: true});

// Configuring app
let port = process.env.port || 3030;
const app = express();
app.use(bodyparser.urlencoded({extended: true}));
app.use(bodyparser.json());
app.use(express.static(__dirname + '/public'));
app.use(flash());
app.use(session({
  key: 'users',
  secret: 'devfest-abuja-code-challenge',
  resave: false,
  saveUninitialized: false
}));

// Setting view engine as ejs
app.set('view engine', 'ejs');

// Using imported routes
app.use('/',landing);
app.use('/sms',sms);
app.use('/call',call);

// Opening port
app.listen(port,() => {
  console.log(`App listening on ${port}`);
})