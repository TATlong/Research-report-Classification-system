#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:59:26 2018

@author: lilong
"""

from interface import Interface_base
from reptile import Report
from word2vec import Word2vec
from lstm import  Lstm_nn

import jieba
import numpy as np
import yaml
from keras.models import model_from_yaml
from gensim.models.word2vec import Word2Vec



class Main_test(Interface_base):
    
    def __init__(self): 
        Interface_base.__init__(self) # 初始化父类
        
    def get_w2v_report(self):  # word2vec训练时的文本存储路径
        report_obj=Report(self.filedir_train)
        report_obj.get_report_page(self.train_start_p,self.train_end_p)
        
    def get_test_report(self,test_start_date,test_end_date): 
        report_obj=Report(self.filedir_test)   # 测试最新研报的文本存储路径
        report_obj.get_report_date(test_start_date,test_end_date)
        self.get_cla_rep()
    
    def get_w2v_train(self):
        w2v=Word2vec()    
        w2v.train()
    
    def get_lstm_train(self):
        lstm=Lstm_nn()      
        lstm.train()

    
    # 研报预测
    def get_cla_rep(self):              
        print ('loading trained model......')
        with open(self.lstm_model, 'r') as f:
            yaml_string = yaml.load(f)       
        model = model_from_yaml(yaml_string) # 加载模型
        print ('loading weights......')        
        model.load_weights(self.lstm_weight) # 加载权重
        model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])        
        word_index=np.load(self.word_index)
        word_index=word_index['dic'][()] 
        #self.get_test_report()   #获取要分类的最新研报
        
        # 开始处理要预测的文本
        files_proce=self.load_w2v_file(self.filedir_test)
        pos_num=0
        neu_num=0
        neg_num=0
        sum_=0
        # 遍历所有的测试文件              
        for file in files_proce:
            #text_split=file.split('&')  # 文本标题分割
            #title=''+text_split[0]+','+text_split[1]+','+text_split[2]+':'   # 打印标题         
            files_token=list(jieba.cut(file.replace(' ', '')))
            file_reshape=np.array(files_token).reshape(1,-1)
            file_vec=self.file_test_vec(word_index,file_reshape)
            file_vec.reshape(1,-1)            
            # 模型预测
            result=model.predict_classes(file_vec)   
            #print(result[0])            
            if   result[0]==0: pos_num+=1
            elif result[0]==1: neu_num+=1
            else: neg_num+=1
            sum_+=1
        print ('Total number of texts:',sum_,'\n'
               ' pos :{:.2%}'.format(pos_num/sum_),'\n',
               'neu :{:.2%}'.format(neu_num/sum_),'\n',
               'neg :{:.2%}'.format(neg_num/sum_))
            
            
            
            

            

#target=Main_test() 
#target.get_w2v_report() # word2vec的训练研报获取
#target.get_w2v_train()  # word2vec开始训练
#target.get_lstm_train() # lstm模型训练
#target.get_test_report('2018-11-5','2018-11-11') # 获取要分类的最新研报起始和终止的时间

#target.get_cla_rep()    # 基于训练好的lstm模型分类新的研报 




'''
if   result[0]==0: 
    print (title,'pos')
elif result[0]==1: 
    print (title,'neu')
else:  print(title,'neg')
'''




      