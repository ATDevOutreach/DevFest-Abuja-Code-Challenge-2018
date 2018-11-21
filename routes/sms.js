var options = {
  apiKey: process.env.africastalking_api,
  username: process.env.africastalking_username
}
const express     = require('express'),
      AfricasTalking = require('africastalking')(options),
      router      = express.Router();

let sms = AfricasTalking.SMS

router.post('/send',(req,res) => {
  const options = {
    to: ['+2347033253198'],
    message: req.body.message
  }

  // Send message and capture the response or error
  sms.send(options)
  .then( response => {
      console.log(response);
      req.flash('success', 'Message sent successfully');
      res.redirect('../home')
  })
  .catch( error => {
      console.log(error);
  });
})


module.exports = router