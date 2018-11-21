const express     = require('express'),
      User        = require('../model/user'),
      bcrypt      = require('bcrypt-nodejs'),
      router      = express.Router();


router.get('/',(req,res) => {
  res.render('landing', {message: req.flash('error')});
});

router.get('/home', sessionChecker, (req,res) => {
  res.render('homePage',{message: req.flash('success')});
});

router.get('/register',(req,res) => {
  res.render('register', {message: req.flash('error')});
});

router.post('/register', (req,res) => {
  let body = req.body;
  if (body.password !== body.c_password) {
    req.flash('error','Passwords don\'t match');
    res.redirect('/register');
  } else {
    bcrypt.genSalt(10,(err,salt) => { //generating salt using bcrypt
      bcrypt.hash(body.password, salt, null, (error,hash) => { //Hashing the password
        // Creating new user object
        let newUser = {
          name: body.name,
          username: body.username,
          password: hash,
          salt: salt
        };
        // Save new user to database
        User.create(newUser, (failed,saved) => {
          if (failed) {
            req.flash('error','Something went wrong');
            res.redirect('/');
          } else {
            // Create new user session
            req.session.user = body.username;
            req.flash('success', `Welcome ${body.name}`);
            res.redirect('/home');
          }
        });
      });
    });
  }
});

router.post('/login', (req,res) => {
  let body = req.body;
  User.findOne({username: body.username}, (err,user) => {
    if (err) {
      req.flash('error','Something went wront, please try again later');
      res.redirect('/login');
    } else if (!user) {
      req.flash('error','Error logging in');
      res.redirect('/login');
    } else {
      bcrypt.compare(body.password, user.password, (error, response) => {
        if(response){
          req.session.user = body.username;
          req.flash('success', `Welcome ${user.name}`);
          res.redirect('/home'); //redirect to home page
        } else {
          req.flash('error','Incorrect username/password');
          res.redirect('/');
        }
      })
    }
  })
});

// Middleware function to check if user session exists
function sessionChecker(req, res, next) {
  if (!req.session.user) {
    req.flash('error','You have to be logged in first')
    res.redirect('/');
  } else {
    next();
  }    
}

module.exports = router;