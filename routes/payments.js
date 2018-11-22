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
    productName: 'MyProduct',
    phoneNumber: '+2348033723897',
    currencyCode: 'NGN',
    amount: 500,
    metaData: {name: 'Abubakre Abdulqudus'}
  }

  // Make the call
  // payment.mobileCheckout(options)
  // .then(response => {
  //     console.log(response);
  // }).catch(error => {
  //     console.log(error);
  // });
})


module.exports = router