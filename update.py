#!/usr/bin/env python
# coding=utf-8
import os
import time

def listDir(path):
    result = []
    for file in os.listdir(path):
        if file[0] == '.': continue
        temp_path = os.path.join(path, file)
        if os.path.isdir(temp_path): 
            result.extend(listDir(temp_path))
        else:
            result.append(temp_path) 

    return result


def file_changed(path):
    files = listDir(path)
    if not len(files): return []
    time_now = list(time.localtime(time.time()))
    result = []
    for file in files:
        statinfo = os.stat(file)
        time_file = list(time.localtime(statinfo.st_ctime))
        if(time_compare(time_file, time_now)):
            result.append(file)
    return result


def time_compare(file_time, time_now):
    file_time[2] += 1
    for i in range(4):
        if file_time[i] > time_now[i]:
            return False
    return True
    # return time_now[2] != file_time[2]


if __name__ == '__main__':
    print(file_changed('../word_count/'))