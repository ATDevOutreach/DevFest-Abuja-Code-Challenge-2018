let hideAlert = () => {
  document.getElementById('alertDialog').style.display = 'none';
}

let previousInput = 'sms';

function changeType (id) {
  if (previousInput !== id) {
  // let formType1 = id === 'sms' ? 'payment' : 'sms' ;
  // let btn = document.getElementById(id);
  // let formType2 = document.getElementById(`${formType1}-form`);
  // console.log(`#${formType1}-form`);
    $(`#payment-form`).toggle('slow');
    $(`#sms-form`).toggle('slow');
    previousInput = id;
  }
  // if (formType.style.display === 'none') {
  //   formType.style.display = 'block';
  //   console.log();
  // } else {
  //   formType.style.display = 'none';
  // }
}