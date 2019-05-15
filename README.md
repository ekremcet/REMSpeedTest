# REMSpeed -  Network Speed Testing Using Websockets

REMSpeed is a network speed testing tool written in Python and JavaScript. It allows you to measure your ping, download and upload speeds by using minimal amount of data.

![Screenshot of Page](https://github.com/ekremcet/SpeedTest/blob/master/remspeed.png?raw=true "Hey")

## Installation

First, you need Python3 in your server and some additional libraries. <br>
**django, django-crispy_forms and websocket_server**
>pip3 install django django-crispy_forms websocket_server

Then you need to open HTTP port and 3 TCP ports on your server. If you want to use default settings open ports **80** and **33333-35**. <br>
## Running the Server
You will need 3 instances of python program. There is a bash script that does that (**run_server.sh**) in the repo. However, if you want to go with different ports you need to modify the arguments accordingly. <br>
You will also need to host the website. To do that you need to run **manage.py** with sudo privileges. <br>
> sudo python3 manage.py runserver 0.0.0.0:80

If you want to measure TCP socket level speed, you can run **tcp_server.py** on the server and **tcp_client.py** on your client. 

## Running Tests
Once the server is up, you can go to your server's public ip address in your browser and click the button to run tests. <br>
Note that due to client side data sending size limitation, upload speed testing in Google Chrome does not work at the moment. We recommend using **Mozilla Firefox.** 


