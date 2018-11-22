# Wallet
Wallet is a simple mobile money app that lets people transfer money to other mobile users from their phones.
An OTP code is sent the user on each transfer to authorize.
The recipient is notified by email when they receive money.
Users can view their balance.

To run:
**Note**: Wallet has been packaged to run on Docker. The build script `build.sh` assumes an OS with Bash installed (Linux/MacOS). If on Windows, you might have to modify it as necessary or run in bash shell installed by Git.
Ensure the `build.sh` and `run.sh` scripts are executable.

  * Create a file `.env` with the following variables:
  * `AT_URL`: The Africa's Talking SMS API URL
  * `AT_USERNAME`: Your Africa's Talking API username
  * `AT_API_KEY`: Your Africa's Talking API key
  * `DB_PASSWORD`: The MySQL database password
  * `DB_USERNAME`: The MySQL database username
  * Run the startup script
    `$ ./build.sh`

Now you can send requests to [`localhost:4000/ussd_handler`](http://localhost:4000/ussd_handler).

