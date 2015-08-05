#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

def main():
    receiver = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3]

    if receiver != "":
        cmd = "sh alarm.sh \"%s\" \"%s\" \"%s\"" % (receiver, title, content)
        os.system(cmd)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "wrong parameters"
        sys.exit()
        pass
    try:
        main()
    except Exception, e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
