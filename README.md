An attempt to access Africa's Talking USSD feature to interact with a Node App.

To get started, 

- Clone this project 
- cd at-demo on you terminal/command prompt/cmd
- run npm install
-sign up on pusher.com and africastalking.com

Download ngrok from www.ngrok.com. Navigate to the directory with ngrok in the command line and expose this cloned project to your local server with:

    ./ngrok http 3000

Once the session status on the ngrok dashboard in the command line interface goes to online, a forwarding address is issued. This is the temporary web address for our app.

Since this address is available on the internet, our POST endpoint is https://url-created.io/order. This is the endpoint required by Africa’s Talking.

Log-in to AfricasTalking and go to the sandbox app. In the sandbox, create a service code and pass in the callback URL of your API endpoint. Our USSD code is now available for use. In the sandbox app, navigate to the ‘launch simulator’ tab and input a valid telephone number to use the USSD feature. All these should be done while your local server is running and ngrok is online.

Once you dial the USSD code in the simulator, fill out the text fields with the chosen data and, once the responses are complete, the dashboard automatically updates with the new order.