var Pusher = require('pusher')
var credentials = require('./config')
var africatalking = require('africastalking')(credentials.AT)
var cors = require('cors')
var bodyParser = require('body-parser')


var express = require('express')
var path = require('path')
var port = 3000
var app = express()

var pusher = new Pusher(credentials.pusher)
app.use(cors())
app.use(bodyParser.urlencoded({extended:false}))
app.use(bodyParser.json())

app.get('/', function(req,res){
	res.sendFile(path.join(__dirname + "/index.html"))
})

app.use(express.static(__dirname + '/'))

var webUrl = 'https://at-demo.food/menu'
var welcomeMsg = "CON Hello! You are welcome Have your food delivered in no time. \n Check out our Menu ${webUrl} \n Enter your name to continue"


var orderDetails = {
    name: "",
    description: "",
    address: "",
    telephone: "",
    open: true
}
var lastData = "";

app.post('/order', function(req, res){
    console.log(req.body);
    var message = 'Hello' 

    var sessionId = req.body.sessionId
    var serviceCode = req.body.serviceCode
    var phoneNumber = req.body.phoneNumber
    var text = req.body.text
    var textValue = text.split('*').length

    if(text === ''){
        message = welcomeMsg
    }else if(textValue === 1){
        message = "CON What would you like to eat?"
        orderDetails.name = text;
    }else if(textValue === 2){
        message = "CON Where can it be delivered to?"
        orderDetails.description = text.split('*')[1];
    }else if(textValue === 3){
        message = "CON Contact number?"
        orderDetails.address = text.split('*')[2];
    }else if(textValue === 4){
        message = `CON Would you like to confirm this order?
        1. Yes
        2. No`
        lastData = text.split('*')[3];
    }else{
        message = `END Thank you for your order`
        orderDetails.telephone = lastData   
    }
    
    res.contentType('text/plain');
    res.send(message, 200);

    console.log(orderDetails)
    if(orderDetails.name != "" && orderDetails.address != '' && orderDetails.description != '' && orderDetails.telephone != ''){
        pusher.trigger('orders', 'customerOrder', orderDetails)
    }
    if(orderDetails.telephone != ''){
        //reset data
    orderDetails.name= ""
    orderDetails.description= ""
    orderDetails.address= ""
    orderDetails.telephone= ""
    }

})
//listen on port 
app.listen(port, function(err, res){
    if(err) throw err
    console.log("Your app is running on http://127.0.0.1:" + port)
})

