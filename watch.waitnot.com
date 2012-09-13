#!/bin/bash
h=waitnot.com; whois $h | grep -q Expiration || echo $h is available\! | /yourpath/bin/sms.py -q
