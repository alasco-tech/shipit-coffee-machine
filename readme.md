# Alasco Coffee Watcher

Hardware setup to watch our espresso machine and let people know when there's fresh delicious coffee being brewed!

In times of distancing, we take the following precaution around our espresso machine: 
If you use the machine, wear a face mask and gloves, 
announce it to the #random channel and serve espresso (via an espresso table) 
-- for everyone showing up in response to the slack notification.

To smoothen this process, the coffee grinder automatically posts to slack when coffee is about to be prepared:


We also include a snap photo of the person preparing the espresso, to make the slack post more engaging and fun.

## Overview
We use a [Voltcraft SEM6000](https://www.conrad.de/de/p/voltcraft-sem6000-energiekosten-messgeraet-bluetooth-schnittstelle-datenexport-datenloggerfunktion-trms-stromtarif-e-1558906.html) smart power plug to monitor power consumption of the coffee grinder. 
Detecting use via power consumption has the advantage of not interfering with the cleaning process of the coffee machine.
The Voltcraft SEM6000 is an easy to use device, because somebody make a very nice shell script to contrrol it from a Linux machine.

A [Raspberry Pi](https://www.raspberrypi.org/) monitors the real time power consumption reported by the smart plug and to detect power spikes.
When detecting usage it takes a picture via the [Pi Camera Module](https://www.raspberrypi.org/products/camera-module-v2/) 
and posts the picture to slack, along with a message.
It additionally counts the number of espressi made and reports it to [Datadog](https://www.datadoghq.com/) for monitoring.

## Slack Bot
Make sure to follow the tutorial of the official python [slackclient](https://github.com/slackapi/python-slackclient) to set up a slack bot that will be allowed to post on your behalf. The created credentials are needed in the `config.ini`!

## Running It
Rename the `config.ini.example` to `config.ini` and ensure to add your slack-bot secrets as `slack_token`, and, optionally, your Datadog token.