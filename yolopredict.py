#!/usr/bin/env python

from subprocess import Popen, PIPE
import os
from texttable import Texttable
from collections import OrderedDict
from operator import itemgetter


currentwd = os.getcwd()
private = currentwd + '/dataset/private'
public = currentwd + '/dataset/public'

def detect_with_yolo(workingdir, imgpath, objtype):
    mydict = {}

    #i = 0
    for image in os.listdir(imgpath):
        if(image.endswith(('.png', '.jpg', '.jpeg'))):
            p = Popen(['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights',
            imgpath + '/' + image], cwd = workingdir, stdout = PIPE, stderr = PIPE)
            stdout, stderr = p.communicate()
            response = stdout.decode("utf-8")

            # Split the whole string by newline and extract the lines with the predictions
            for item in response.split("\n"):
                if "%" in item:
                    obj = item.split(":")[0].strip()
                    if not obj in mydict:
                        mydict[obj] = 1
                    else:
                        mydict[obj] += 1
            # We just wanted to run for the first 10 images
            #i = i + 1
            #if(i == 10):
            #    break

    # Lets print a table
    tab = Texttable()
    header = [objtype +' Object', 'No of Occurence']
    tab.header(header)
    tab.set_cols_width([25,20])
    tab.set_cols_align(['c','c'])
    tab.set_cols_valign(['m','m'])
    tab.set_deco(tab.HEADER | tab.VLINES)
    tab.set_chars(['-','|','+','#'])

    # LEts Sort the Dictionary
    ordered = OrderedDict(sorted(mydict.items(), key=itemgetter(1), reverse=True))
    for result in ordered:
        row = [result,ordered[result]]
        tab.add_row(row)

    # Lets draw the table
    s = tab.draw()
    print s
    print "\n\n"


# Call the function for private images

detect_with_yolo(currentwd, private, "Private")
detect_with_yolo(currentwd, public, "Public")
