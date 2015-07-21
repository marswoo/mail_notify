#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import simplejson as json


def main():
    date = sys.argv[1]  # configure file
    taskname = sys.argv[2]  # time
    type = sys.argv[3]  # run test debug

    conf_file = "../task/" + taskname + "/conf/mail/mail.json"
    report_file = "../task/" + taskname + "/report/" + str(date) + \
        "/report.html"

    if os.path.exists(conf_file):
        fc = open(conf_file, 'r')
        conf = fc.read()
        fc.close()
        confJson = json.loads(conf.strip())
        mail_receiver = confJson["mail_receiver"]
        debug_mail_receiver = confJson["debug_mail_receiver"].encode('utf8')
        test_mail_receiver = confJson["test_mail_receiver"].encode('utf8')
        title = str(date) + " " + confJson["title"].encode('utf8')

        fin = open(report_file, 'r')  # the file of pipeline
        content = fin.read()
        fin.close()
        # print mail_receiver,debug_mail_receiver,test_mail_receiver
        if(type == "debug"):
            receiver = debug_mail_receiver
        elif (type == "test"):
            receiver = test_mail_receiver
        elif(type == "run"):
            receiver = mail_receiver

        # check err.log of data_processor stage
        log_file_dataprocessor = "../task/" + taskname + "/data_processor/log/"\
            + str(date)+"/err.log"
        if os.path.exists(log_file_dataprocessor):
            fin = open(log_file_dataprocessor, 'r')
            errcontent = fin.read()
            fin.close()
            if errcontent:
                receiver = debug_mail_receiver
                err_title = "Error : " + title
                errcontent = " ".join(("There is something wrong",
                                       "in data_process stage :",
                                       errcontent))
                cmd = "sh alarm.sh \"%s\" \"%s\" \"%s\" " % (receiver,
                                                             err_title,
                                                             errcontent)
                os.system(cmd)
                sys.exit(2)
        # check err.log of generate report stage
        log_file_report = "./log/" + str(date) + "/err.log"
        if os.path.exists(log_file_report):
            fin = open(log_file_report, 'r')
            errcontent = fin.read()
            fin.close()
            if errcontent:
                receiver = debug_mail_receiver
                err_title = "Error : " + title
                errcontent = " ".join(("There is something wrong",
                                       "in generate report stage :",
                                       errcontent))
                cmd = "sh alarm.sh \"%s\" \"%s\" \"%s\" " % (receiver,
                                                             err_title,
                                                             errcontent)
                os.system(cmd)
                sys.exit(2)

        # common status of sending email
        if (receiver != ""):
            cmd = "sh alarm.sh \"%s\" \"%s\" \"%s\"" % (receiver,
                                                        title,
                                                        content)
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
