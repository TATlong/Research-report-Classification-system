#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:12:06 2018

@author: lilong
"""
from  main_test import  Main_test


target=Main_test() 

# 如果本地已经保存，这里就不需要重新获取,直接调用模型预测：arget.get_cla_rep
target.get_test_report('2018-11-11','2018-11-12') # 获取要分类的最新研报起始和终止的时间
#target.get_cla_rep()    # 基于训练好的lstm模型分类新的研报 


