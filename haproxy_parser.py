#!/usr/bin/python
# -*- coding: utf-8 -*-
#Show tree frontend->backend->servers
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
#from pprint import pprint
import json
import argparse

parser = argparse.ArgumentParser(description='Parse haproxy.cfg file')
parser.add_argument('type', metavar='T', type=str, help='type: text or json', choices=['text','json'], default='text', nargs='?')
parser.add_argument('-f', type=str, default='haproxy.cfg',help='file path')
parser.add_argument('-i', type=int, default='4',help='indent')
args = parser.parse_args()
print args.type, args.f

out_type=args.type
default_indent=args.i

cfg_parser = Parser(args.f)
configuration = cfg_parser.build_configuration()

# get frontends
frontends = configuration.frontends

ha_conf={}
#iterate frontends
for i in frontends:
  if(out_type == 'text'):
    print i.name, i.host, i.port
  if(out_type == 'json'):
    d={}; d['port']=i.port; d['host']=i.host;
    d['backends']=[]
    ha_conf[i.name]=d
  backends = i.usebackends()
  for z in backends:
    if(out_type == 'text'):
      print " "*(default_indent-1), z.backend_name, z.operator, z.backend_condition
      #print "Is default",z.is_default
    if(out_type == 'json'):
      s={}; s['backend_name']=z.backend_name; s['operator']=z.operator;s['backend_condition']=z.backend_condition;
      s['servers']=[]
    bac_conf = configuration.backend(z.backend_name)
    servers = bac_conf.servers()
    for y in servers :
      if(out_type == 'text'):
        print " "*(2*default_indent-1), y.name, y.host, y.port, y.attributes
      if(out_type == 'json'):
        ss={}; ss['name']=y.name; ss['host']=y.host; ss['port']=y.port; ss['attributes']=y.attributes;
        s['servers'].append(ss)
    if(out_type == 'json'):
      d['backends'].append(s)

if(out_type == 'json'):
  #print json
  print json.dumps(ha_conf,sort_keys=True,indent=default_indent,);
