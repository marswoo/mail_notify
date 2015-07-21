#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import traceback
import simplejson as json

def main():

    pipeline = sys.argv[1]  #pipeline configure file
    date = sys.argv[2]  #time of sending email
    dir_root = os.path.dirname(pipeline)

    data_dir = dir_root + '/data_processor/data/' + date + '/'
    report_path = dir_root + '/report/' + date + '/body.html'

    fout = open(report_path, 'w')
    fout.close()
    fout = open(report_path, 'w+')

    fp = open(pipeline, 'r') #the file of pipeline
    content_pipeline = fp.readline()
    fp.close()
    content = content_pipeline[5:].strip() #因为content_pipeline以“body=”开头
    conf_files = content.split('->')

    for file in conf_files:
        file_path = dir_root + '/conf/body/' + file
        if os.path.exists(file_path):
            fin = open(file_path, 'r')
            conf = fin.read()
            fin.close()
            confJson = json.loads(conf.strip())
            type = confJson['type']
            if(type == 'table'):
                creat_table(confJson, file, data_dir, fout)
            elif (type == 'span'):
                creat_span(confJson, file, data_dir, fout)
            elif (type == 'text'):
                creat_text(confJson, file, data_dir, fout)
            fout.write("<br>\n");
    fout.close()

def creat_table(confJson, file, data_dir, fout):
    if  not confJson.has_key('title') or not confJson.has_key('data_file') \
    or not confJson.has_key('data_column_attribute') or not confJson.has_key('column_name'):

        print "parameter is missing"
        return 0

    title = confJson['title'].encode('utf8')
    df = confJson['data_file']
    nf = confJson['notation_file'] 
    ca = confJson['data_column_attribute']
    cn = confJson['column_name']
    cv = confJson['column_value']
    count = len(ca)

    fout.write("<p> %s </p>\n<table class=\"hovertable\">\n<tr>\n\t" %title)
    for name in cn:
        fout.write("<th>%s</th>"  %name.encode('utf8'))  
    
    fout.write("\n</tr>\n")

    data_path = data_dir + df
    if not os.path.exists(data_path):
        print "datefile %s is not exsit!" %data_path
        return 0
    else:
        fin = open(data_path)

    for line in fin:
        arr = line.strip().split('\t')
        for value in cv:
            fout.write("<td> ")
            for v in value:
                if(ca[v] == "string"):
                    fout.write("%s" %arr[v])
                elif(ca[v] == "int"):
                    fout.write("%d" %int(arr[v]))
                elif(ca[v] == "float"):
                    fout.write("%.3f" %float(arr[v]))
                elif (ca[v] == "percent"):
                    cmpstr = "%.2f"  %(abs(float(arr[v])) * 100) + "%"
                    fout.write("%s" %cmpstr)

                elif (ca[v] == "arrow"):
                    if float(arr[v]) == 0:
                        cmpstr = "&nbsp;-&nbsp;-"
                    elif float(arr[v]) > 0:
                        cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='red'>&uarr;</font>"
                    else:
                        cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='green'>&darr;</font>"

                    fout.write("%s" %cmpstr)
            fout.write("</td>")

        fout.write("\n</tr>\n")

    fout.write("</table>\n")
    fin.close()

    notation_path = data_dir + nf
    if not os.path.exists(notation_path) or nf == "":
        print "notation %s is not exsit!" %notation_path
    else:
        fin = open(notation_path)
        notation = fin.read()
        fout.write("<font size=2>")
        fout.write("%s" %notation)
        fout.write("</font><br>\n")
        fin.close()

    fout.write("\n\n")


def creat_span(confJson, file, data_dir, fout):
    if  not confJson.has_key('title') or not confJson.has_key('data_file') \
    or not confJson.has_key('data_column_attribute') or not confJson.has_key('column_name'):

        print "parameter is missing"
        return 0

    title = confJson['title'].encode('utf8')
    df = confJson['data_file']
    nf = confJson['notation_file'] 
    ca = confJson['data_column_attribute']
    cn = confJson['column_name']
    cv = confJson['column_value']
    cc = confJson['combined_column']
    field_desc = confJson.get('field_desc', None)
    count = len(ca)

    fout.write("<p> %s </p>\n<table class=\"hovertable\">\n<tr>\n\t" %title)
    for name in cn:
        fout.write("<th>%s</th>"  %name.encode('utf8'))  
    
    fout.write("\n</tr>\n")

    if field_desc is not None:
        fout.write("<tr style=\"text-align:center\;color:blue\">\n")
        #fout.write("<tr>\n")
        for desc in field_desc:
            fout.write("<td>%s</td>"  %desc.encode('utf8'))
        fout.write("\n</tr>\n")

    data_path = data_dir + df
    if not os.path.exists(data_path):
        print "datefile %s is not exsit!" %data_path
        return 0
    else:
        fin = open(data_path)
    
    data = []
    location = {}
    mark = {}
    scount = {}
    list = {}
    count = 0
    for line in fin:
        arr = line.strip().split('\t')
        data.append(arr)

    for comb in cc:
        pre = ""
        location[comb] = []
        for arr in data:
            if(arr[comb] == pre):
                count = count + 1
            else:
                if (pre != ""):
                    location[comb].append(count)
                    pre = arr[comb]
                    count = 1
                else:
                    pre = arr[comb]
                    count = 1
        location[comb].append(count)
        mark[comb] = 0
        scount[comb] = 0
        list[comb] = 0
        
    for arr in data:
        for value in cv:
            flag = value[0]
            if(location.has_key(flag)):
                if(mark[flag] == 0):
                    fout.write("<td rowspan=\"%s\"> " %location[flag][list[flag]])
                    scount[flag] = scount[flag] + 1
                    mark[flag] = 1
                    for v in value:
                        if(ca[v] == "string"):
                            fout.write("%s" %arr[v])
                        elif(ca[v] == "int"):
                            fout.write("%d" %int(arr[v]))
                        elif(ca[v] == "float"):
                            fout.write("%.3f" %float(arr[v]))
                        elif (ca[v] == "percent"):
                            cmpstr = "%.2f"  %(abs(float(arr[v])) * 100) + "%"
                            fout.write("%s" %cmpstr)
                        elif (ca[v] == "arrow"):
                            if float(arr[v]) == 0:
                                cmpstr = "&nbsp;-&nbsp;-"
                            elif float(arr[v]) > 0:
                                cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='red'>&uarr;</font>"
                            else:
                                cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='green'>&darr;</font>"
                            fout.write("%s" %cmpstr)
                    fout.write("</td>")
                else:
                    scount[flag] = scount[flag] + 1
                if(scount[flag] == location[flag][list[flag]]):
                    scount[flag]= 0
                    mark[flag] = 0
                    list[value[0]] = list[value[0]] + 1


            else:
                fout.write("<td> ")
                for v in value:
            
                    if(ca[v] == "string"):
                        fout.write("%s" %arr[v])
                    elif(ca[v] == "int"):
                        fout.write("%d" %int(arr[v]))
                    elif(ca[v] == "float"):
                        fout.write("%.2f" %float(arr[v]))
                    elif (ca[v] == "percent"):
                        cmpstr = "%.2f"  %(abs(float(arr[v])) * 100) + "%"
                        fout.write("%s" %cmpstr)
                    elif (ca[v] == "arrow"):
                        if float(arr[v]) == 0:
                            cmpstr = "&nbsp;-&nbsp;-"
                        elif float(arr[v]) > 0:
                            cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='red'>&uarr;</font>"
                        else:
                            cmpstr = "&nbsp;%.2f"  %(abs(float(arr[v])) * 100) + "%" + "<font color='green'>&darr;</font>"

                        fout.write("%s" %cmpstr)
                fout.write("</td>")

        fout.write("\n</tr>\n")
    fout.write("</table>\n")
    fin.close()

    notation_path = data_dir + nf
    if not os.path.exists(notation_path) or nf == "":
        print "notation %s is not exsit!" %notation_path
    else:
        fin = open(notation_path)
        notation = fin.read()
        fout.write("<font size=2>")
        fout.write("%s" %notation)
        fout.write("</font><br>\n")
        fin.close()

    fout.write("\n\n")



def creat_text(confJson, file, data_dir, fout):
    tf = confJson['text_file']

    text_path = data_dir + tf
    if not os.path.exists(text_path) or tf == "":
        print "text %s is not exsit!" %text_path
    else:
        fin = open(text_path)
        text = fin.read()
        fout.write("%s<br>\n\n\n" %text)
        fin.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "wrong parameters"
        sys.exit()
        pass
    try:
        main()
    except Exception, e:
        traceback.print_exc()
        sys.exit(2)
