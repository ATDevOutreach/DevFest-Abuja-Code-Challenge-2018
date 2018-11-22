var options = {
  apiKey: process.env.africastalking_api,
  username: process.env.africastalking_username
}
const express     = require('express'),
      AfricasTalking = require('africastalking')(options),
      router      = express.Router();

let payment = AfricasTalking.PAYMENTS

router.post('/',(req,res) => {
  const options = {
    productName: 'MyProduct', // The name of a demo product created in my sandbox app
    phoneNumber: req.body.number,
    currencyCode: req.body.currency,
    amount: req.body.amount,
    metaData: {name: 'Abubakre Abdulqudus'}
  }
  
  // Make the call
  payment.mobileCheckout(options)
  .then(response => {
      console.log(response);
      // show flash message if payment is successfully made
      req.flash('success', 'Message sent successfully');
      res.redirect('../home');
  }).catch(error => {
      console.log(error);
      req.flash('success', 'Message sent successfully');
      res.redirect('../home');
  });
})


module.exports = router