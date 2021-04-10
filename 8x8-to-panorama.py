#!/usr/bin/env python3

import panos
import argparse
import getpass
import json

def connect(panorama):
  username = getpass.getuser()
  password = getpass.getpass()
  return pano = panorama.Panorama(panorama, username, password)

def parseDomains(data, panorama):
  print('parse domains')
  print(data)

def parseSubnets(data, panorama):
  print('Detected json as subnets, parsing')
  # pano = connect(panorama)
  # Change to Firewall
  # fw.add(objects.AddressObject("Server", "2.2.2.2")).create()
  # Change to Panorama
  # pano.add(panorama.DeviceGroup("CustomerA")).create()
  # The create() method will never remove a variable or object, only add or change it.
  pano.add(panorama.DeviceGroup("CustomerA")).create()


def main(args):
  if args.filename:
      # open the file and load as json data
      with open(args.filename[0]) as f:
        data = json.load(f)
        # check if it's a list of domains or subnets 
        if data[0].get('DomainName'):
          parseDomains(data, args.panorama[0])
        elif data[0].get('Subnet'):
          parseSubnets(data, args.panorama[0])
        else:
          print('Could not parse json. Please check source file')
          exit(0)
  else:
    print('Please specify a filename with -f')
    exit(0)
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', nargs='+', help='Specify json file to import')
    parser.add_argument('-p', '--panorama', nargs='+', help='Specify Panorama IP or hostname')
    args = parser.parse_args()
    main(args)