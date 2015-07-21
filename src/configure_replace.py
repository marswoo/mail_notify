#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import simplejson as json
from string import Template

def main():

	conf_file = sys.argv[1]  #configure file
	date = sys.argv[2]  #time
	file_in = sys.argv[3]
	file_out = sys.argv[4]

	if os.path.exists(conf_file):
		fc = open(conf_file, 'r')
		conf = fc.read()
		fc.close()
		confJson = json.loads(conf.strip())
		confJson['DATE'] = date
		for key in confJson.keys():
			confJson[key] = confJson[key].encode('utf8')

	fin = open(file_in, 'r') #the file of pipeline
	content = fin.read()
	fin.close()
	content_ori = Template(content)
	content_final = content_ori.safe_substitute(confJson)


	fout = open(file_out, 'w')
	fout.write(content_final)
	fout.close()

if __name__ == '__main__':
	if len(sys.argv) != 5:
		print "wrong parameters"
		sys.exit()
		pass
	try:
		main()
	except Exception, e:
		import traceback
		traceback.print_exc()
		sys.exit(2)
