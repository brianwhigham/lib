#!/usr/bin/python2.7

# Author: Brian Whigham
# Created 9/13/12
# description: send an sms
# based on: Scott Hillman's scripties at http://everydayscripting.blogspot.com/2009/10/python-google-voice-from-command-line.html
# config file format:
#   [login]
#   email: yourname@gmail.com
#   password: yourpass
#   [options]
#   # used for the default SMS recipient (assuming you like to notify yourself of stuff a lot)
#   forwarding_number: 5555550199

configfile = '/yourpath/etc/googlevoice.conf'
gvoicelibpath = '/yourpath/lib/gvoice'

import sys
# path to https://github.com/hillmanov/gvoice stuff
sys.path.append(gvoicelibpath)
import gvoice
from optparse import OptionParser
import ConfigParser


config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read(configfile)
forwarding_number = None
if config.has_option('options','forwarding_number'):
  forwarding_number = config.get('options','forwarding_number')
email = config.get('login','email')
password = config.get('login','password')

parser = OptionParser()
parser.add_option("-r", "--recipient", help="send SMS to this sms-capable phone number", dest="recipient")
parser.add_option("-m", "--message", help="SMS message body (will be auto-pruned to 140 chars)", dest="message")
parser.add_option("-q", "--quiet", help="Don't print anytyhing to STDOUT", dest="verbose", default=True, nargs=0)

(options, args) = parser.parse_args()

if not options.message:
  inputrequest = "You must provide a message (-m)! You may provide one now: "
  if not options.verbose: inputrequest = ""
  options.message = raw_input (inputrequest)

if not options.recipient:
  if forwarding_number:
    options.recipient = forwarding_number
  else:
    print "You must provide an sms-capable number to send the message to (-r).  The number can be stored in the config file as 'forwarding_number' in the options section."
    exit()

# not too long!
message = options.message[:139]

gv_login = gvoice.GoogleVoiceLogin(email, password)
text_sender = gvoice.TextSender(gv_login)

text_sender.text = options.message
text_sender.send_text(options.recipient)

if text_sender.response and options.verbose:
  print 'Success! Message sent!'
elif options.verbose:
  print 'Failure! Message not sent!'
