#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from del_Ds_store import Del_store
#from os.path import isfile, join



class Rename(object):
    
       
    def __init__(self,path_proce,num):        
        self.path_proce=path_proce
        self.num=num
        Del_store().file_filter() # 初始化类时删除.Del_store文件
        self.transform_file()
    
    # 创建文件夹
    def create_directory(self,filename):
        path = os.getcwd()  # 获得当前的目录 os.chdir('E:'):切换到指定目录                                 
        target_path = os.path.join(path, filename)   # 将子目录放在根目录下面   
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        return target_path
    
    # 加载训练文件
    def transform_file(self):  
        print('dir_now_1:',os.getcwd())   
        dir_now=os.chdir(os.getcwd()+'/'+self.path_proce)
        print('dir_now_2:',os.getcwd())
        print(os.listdir('./'))               
        for item in os.listdir(dir_now):
            d1=os.getcwd()+'/'+item
            print('dir:',d1)
            num=self.num
            for f in os.listdir(d1):               
                oldname=d1+'/'+f               
                newname=d1+'/'+'{}.txt'.format(item+'_'+str(num))                
                os.rename(oldname,newname)
                num=num+1
 

'''       
# path_proce:需要重新命名的文件路径
path_proce='manual_classification'
tt=Rename(path_proce,1)
'''



    