#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:39:38 2018

@author: lilong
"""

import os, sys;


class Del_store(object):
    
    def walk(self,path):
        for item in os.listdir(path):
            try:
                if(item == ".DS_Store"): 
                    os.remove(path+"/"+item)
                else:
                    # 判断当前路径下的文件夹，循环嵌套判断文件夹下的.Ds_store文件
                    if(os.path.isdir(path+"/"+item)):
                        self.walk(path+"/"+item)
                    else: pass
            except OSError:
                print('wrong !')
                        
    def file_filter(self):
        print(sys.argv)
        if(len(sys.argv)>1):
            root_dir = sys.argv[1]
        else:
            root_dir = os.getcwd()          
        self.walk(root_dir)  # root_dir是该del_Ds_store.py文件的路径


'''
tt=Del_store()  
tt.file_filter()
'''