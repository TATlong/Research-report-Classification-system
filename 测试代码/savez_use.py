#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 19:26:22 2018

@author: lilong
"""

import numpy as np


# 简单的数组保存
arr = np.array([[1, 2], [3, 4]])
np.save('/Users/lilong/Desktop/mm.npy',arr)
arr_load=np.load('/Users/lilong/Desktop/mm.npy')
print(arr_load,'\n\n',arr_load[0])


# 非结构化数据保存
str_ = 'abc'
arr_ = np.array([[1, 2], [3, 4]])
dict_ = {'a' : 1, 'b': 2}
np.savez('/Users/lilong/Desktop/nn.npz', st= str_, ar = arr_, dic= dict_)


data = np.load('/Users/lilong/Desktop/nn.npz')
print('....\n',data['st'],'\n',data['st'][()])
print('....\n',data['ar'],'....\n',data['ar'][0],'\n\n',data['ar'][()][0])
print('....\n',data['dic'],'\n\n',data['dic'][()])
#print('....\n',data['dic']['a'])  # 报错
print('....\n',data['dic'][()]['a'])
