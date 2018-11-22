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
  console.log(options);
  // Make the call
  // payment.mobileCheckout(options)
  // .then(response => {
  //     console.log(response);
  // }).catch(error => {
  //     console.log(error);
  // });
})


module.exports = router