# -*- coding: utf-8 -*-

""" Command and Control Server

Usage:

  $ python server.py [-h|--help]

"""
import argparse
import socket


# Default host name.
HOST_NAME = ''

# Default message buffer size.
BUFFER_SIZE = 1024


def get_command_line_parser():
  """ Returns a command line parser for the command and control server.

  Returns:
    argparse.ArgumentParser: A command line parser.
  """
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'port_number',
    type=int,
    help='the port number of the command and control server',
  )

  return parser


def main():
  """ Runs the command and control server. """
  parser = get_command_line_parser()
  args = parser.parse_args()

  UDPSock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  UDPSock.bind((HOST_NAME, args.port_number))

  while True:
    data, _ = UDPSock.recvfrom(BUFFER_SIZE)
    print data

  #UDPSock.close()


if __name__ == '__main__':
  main()

