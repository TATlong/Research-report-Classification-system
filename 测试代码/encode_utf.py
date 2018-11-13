#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:42:29 2018

@author: lilong
"""


import chardet
import os


class Unicode(object):
     
    def __init__(self):
        self.file_path='/Users/lilong/Desktop/coding_test/'
        self.flag=0
    
    def readFile(self,file_path):
        with open(file_path, 'rb') as f:  # 这里读文件判断编码时必须是‘rb’的格式
            filecontent = f.read()
        return filecontent
    
    def converCode(self,filepath):
        file_con = self.readFile(filepath)
        result=chardet.detect(file_con)  # 判断文件编码
        print('result:',result)
        if self.flag==0:            
            if result['encoding'] == 'GB2312':  # GBK是GB2312的扩展                
                unicode_raw = file_con.decode('GB2312')  # unicode_raw是字节流
                unicode_done= unicode_raw.encode('utf-8')  # unicode_done是字节流
                #print(str(unicode_done))
                with open(filepath, 'wb') as f: # 这里写文件时必须时‘wb’的格式
                    f.write(unicode_done)
        else:
            pass
        
    def listDirFile(self,file_path):
        list_ = os.listdir(file_path)
        for ll in list_:
            filepath = os.path.join(file_path, ll)
            if os.path.isdir(filepath):
                self.listDirFile(filepath)
            else:
                print('ll:',ll)
                self.converCode(filepath)            
    
    def check(self):
        self.flag=1
        self.listDirFile(self.file_path)
    
    def start(self):
        self.listDirFile(self.file_path)
        self.check()


# 实例化
tt=Unicode()
tt.start()

