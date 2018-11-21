var options = {
  apiKey: process.env.africastalking_api,
  username: process.env.africastalking_username
}
const express     = require('express'),
      AfricasTalking = require('africastalking')(options),
      router      = express.Router();

let voice = AfricasTalking.VOICE

router.post('/',(req,res) => {
  const options = {
    // Set your Africa's Talking phone number in international format
    callFrom: '+2347033253198',
    // Set the numbers you want to call to in a comma-separated list
    callTo: ['+23433723897']
  }

  // Make the call
  voice.call(options)
  .then(response => {
      console.log(response);
  }).catch(error => {
      console.log(error);
  });
})


module.exports = router