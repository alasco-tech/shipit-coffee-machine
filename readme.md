# alasco-barista

Our hardware setup to monitor our espresso machine and let people know when there's fresh delicious coffee being brewed!
This is an outcome of one of our quarterly [ShipIt days](https://alasco.tech/2019/07/02/shipit-day-recap.html).


## Overview
In times of social distancing, we adopted the following rule around our espresso machine: 
If you use the machine, wear a face mask and gloves, 
announce it to the #random channel and serve espresso (via an espresso table) 
— for everyone showing up.

To smoothen this process, the coffee grinder automatically triggers a slack message when coffee is about to be prepared:

![Coffee Process Visualization](coffee_process.png)

We also include a of the person preparing the espresso, to make the slack post engaging and fun.

## Hardware Setup
We use a [Voltcraft SEM6000](https://www.conrad.de/de/p/voltcraft-sem6000-energiekosten-messgeraet-bluetooth-schnittstelle-datenexport-datenloggerfunktion-trms-stromtarif-e-1558906.html) smart power plug to monitor the real-time power consumption of the coffee grinder. 

Detecting machine use via power consumption has the advantage of not interfering with the cleaning and maintenance of the coffee machine.
The Voltcraft SEM6000 is an easy to use device for scripting, because somebody made [a very nice command line tool](https://github.com/Heckie75/voltcraft-sem-6000) to control it from a Linux machine.

A [Raspberry Pi](https://www.raspberrypi.org/) monitors the real-time wattage of the coffee grinder reported by the smart plug to observe when the machine is turned on.
When detecting usage, a picture is taken via the [Pi Camera Module](https://www.raspberrypi.org/products/camera-module-v2/) 
and posted to slack, along with a message.
 Additionally, we count the number of espressi made and report it to [Datadog](https://www.datadoghq.com/).

## Software Setup
Starting from a vanilla [Raspberry Pi OS Lite](https://www.raspberrypi.org/downloads/raspberry-pi-os/) installation, set up [SSH and wifi credentials for headless usage](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup).

Check out the alasco barista repository along with [the Voltcraft SEM 6000 script](https://github.com/Heckie75/voltcraft-sem-6000) in `/home/pi` and [follow the instructions](https://github.com/Heckie75/voltcraft-sem-6000) to configure the bluetooth plug as `coffee_grinder`.

Link the service file via `sudo ln -s coffee_watcher.service /etc/systemd/system/` and use `systemctl enable coffee_watcher` to run the watcher script on boot.

## Slack Bot
Make sure to follow the tutorial of the official [python-slackclient](https://github.com/slackapi/python-slackclient) to set up a slack bot that will be allowed to post on your behalf. The created credentials are needed in the `config.ini`!


Rename the `config.ini.example` to `config.ini` and ensure to add your slack-bot secrets as `slack_token`. Optionally, add your Datadog API key as `dd_api_key`.

