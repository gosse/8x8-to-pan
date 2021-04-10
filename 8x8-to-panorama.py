#!/usr/bin/env python3

from panos import panorama
from panos import objects
import argparse
import getpass
import json

def connect(panoAddress):
  username = input('Username: ' )
  password = getpass.getpass()
  print(panoAddress)
  pano = panorama.Panorama(panoAddress, username, password)
  return pano

def parseDomains(data, panoAddress):
  print('parse domains')
  print(data)

def parseSubnets(data, panoAddress):
  print('Detected json as subnets, parsing')
  pano = connect(panoAddress)
  addresses = []
  for d in data:
    print(d['Subnet'])
    AddressName = '8x8-' + d['Subnet'].replace('/', '-')
    print(AddressName)
    address_object = objects.AddressObject(AddressName, d['Subnet'])
    pano.add(address_object).create()
    addresses.append(address_object)
  pano.add(objects.AddressGroup('8x8 Addresses', addresses))
    
    
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
