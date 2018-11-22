let hideAlert = () => {
  document.getElementById('alertDialog').style.display = 'none';
}

let previousInput = 'sms';

function changeType (id) {
  if (previousInput !== id) { // Checks if ID doesn't match previous input variable
    // Toggle visibility of the form using Jquery 
    $(`#payment-form`).toggle('slow');
    $(`#sms-form`).toggle('slow');
    previousInput = id;
  }
}