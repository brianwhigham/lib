#!/usr/bin/python

# Author: Brian Whigham
# Created 9/13/12
# description: have GV bridge a phone call for you (make a call)
# based on: Scott Hillman's scripties at http://everydayscripting.blogspot.com/2009/10/python-google-voice-from-command-line.html
# Note: you'll get 500 errors if you don't specify a phone type
#   [login]
#   email: yourname@gmail.com
#   password: yourpass
#   [options]
#   forwrding_number: 5555550199
#   phone_type: 2


# phone_type for your forwarding_number is one of
#  1 - Home
#  2 - Mobile
#  3 - Work
#  7 - Gizmo

configfile = '/yourpath/etc/googlevoice.conf'
gvoicelibpath = '/yourpath/lib/gvoice'

import sys
# path to https://github.com/hillmanov/gvoice repo
sys.path.append(gvoicelibpath)
import gvoice
from optparse import OptionParser
import ConfigParser


#config = ConfigParser.RawConfigParser(allow_no_value=True)
config = ConfigParser.RawConfigParser()
config.read(configfile)
forwarding_number = None
phone_type = None
if config.has_option('options','forwarding_number'):
  forwarding_number = config.get('options','forwarding_number')
if config.has_option('options','phone_type'):
  phone_type = config.get('options','phone_type')
email = config.get('login','email')
password = config.get('login','password')

parser = OptionParser()
parser.add_option("-d", "--destination", help="the phone number you want to talk to", dest="destination")
parser.add_option("-f", "--forwardingnumber", help="The GV-registered phone that you want to initiate the call", dest="forwarding_number")
parser.add_option("-t", "--phonetype", help="The phone type of the intiating GV-registered phone (1=home, 2=mobile, 3=work)", dest="phone_type")
parser.add_option("-q", "--quiet", help="Don't print anytyhing to STDOUT", dest="verbose", default=True, nargs=0)

(options, args) = parser.parse_args()

if not options.phone_type:
  if phone_type:
    options.phone_type = phone_type

if not options.forwarding_number:
  if forwarding_number:
    options.forwarding_number = forwarding_number

if not options.destination or not options.forwarding_number or not options.phone_type:
  parser.print_help()
  exit()


gv_login = gvoice.GoogleVoiceLogin(email, password)
number_dialer = gvoice.NumberDialer(gv_login)
number_dialer.forwarding_number = options.forwarding_number
number_dialer.phone_type = options.phone_type
number_dialer.place_call(options.destination)

if number_dialer.response and options.verbose:
   print 'Success! You should hear the phone (' + options.forwarding_number + ') ringing shortly...'
elif options.verbose:
   print 'Call failed!'
