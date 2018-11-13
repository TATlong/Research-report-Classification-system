#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 22:28:41 2018

@author: lilong
"""

from interface import Interface_base


import numpy as np
import pandas as pd
import sys,os


import yaml
from sklearn.cross_validation import train_test_split

from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary

from keras.utils import np_utils
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout,Activation
from keras.models import model_from_yaml
from keras.layers import Flatten
from sklearn.preprocessing import LabelEncoder



class Lstm_nn(Interface_base):
    
    def __init__(self): # 初始化父类
        Interface_base.__init__(self)
        
           
    # 该函数初步处理训练数据
    def splice_data(self,path): 
        sp=np.array([]) # 读取正面样本
        pathdir = os.listdir(path)
        for pf in pathdir:
            newdir = os.path.join(path, pf) # 获取的文件路径
            print('newdir:',newdir)
            # 之这里是‘gbk’的编码，因为人工分类的文本保存用的windows系统
            # 如果人工分类时是mac，那就改成utf-8的编码
            with open(newdir, "r", encoding='gbk') as f: 
                tmp=''                
                lines = f.readlines()                
                for line in lines:                        
                    line=line.strip()
                    line.replace(' ', '')
                    tmp=tmp+line
                sp=np.append(sp,tmp)
        return sp    
    
    
    # 拼接训练文件
    def load_train_file(self):     
        pos=self.splice_data(self.pos_path) # 拼接正样本
        neu=self.splice_data(self.neu_path) # 拼接负样本 
        neg=self.splice_data(self.neg_path) # 拼接负样本                      
        combined=np.concatenate((pos,neu,neg)) # 正和负样本文本的拼接 
        pos_array = np.array([-1]*len(pos),dtype=int)
        neu_array = np.array([0]*len(neu),dtype=int)
        neg_array = np.array([1]*len(neg),dtype=int)             
        y = np.concatenate((pos_array, neu_array,neg_array)) # 正、中性、fu2标签的拼接  
        print(len(y))
        return combined,y  
     
    # 得到每篇文本在词典中的索引列表，不同的文本长度不同，所以列表长度也不同
    def parse_dataset(self,combined):
        w2indx=np.load(self.word_index)
        w2indx=w2indx['dic'][()]  # 必须这种形式读取保存的字典
        w2vec=np.load(self.word_vec)
        w2vec=w2vec['dic'][()]
        data=[]
        for text in combined:
            new_txt = []
            for word in text:
                try:
                    new_txt.append(w2indx[word])
                except:
                    new_txt.append(0)
            data.append(new_txt)
        #print(len(data[0]),len(data[1]))
        return w2indx,w2vec,data
    
    
    # lstm模型训练数据的结构化
    def train_data_struc(self,combined):       
        w2indx,w2vec,struc_w2index=self.parse_dataset(combined) # 在这里是不等长的数列
        # 得到每篇文本所含的词语对应的索引：后端截断并且填0补充
        struc_w2index= sequence.pad_sequences(struc_w2index, maxlen=self.maxlen,padding='post',truncating='post')
        return w2indx,w2vec,struc_w2index
    
    
    # index_dict:所有的词索引列表(词：索引), word_vectors:所有词的词向量, combined:所有文本的索引值
    def get_train_data(self,word_index,word_vectors,struc_w2index,y):
        n_symbols = len(word_index) + 1  # 词典的大小   
        embedding_weights = np.zeros((n_symbols, self.vocab_dim)) # 索引为0的词语，词向量全为0
        # 从索引为1的词语开始，每个词语对应其词向量形成词向量矩阵
        for word, index in word_index.items():
            embedding_weights[index, :] = word_vectors[word]    
        #print('embedding_weights:',embedding_weights[:2]) 
        print(len(struc_w2index),len(y))
        x_train, x_test, y_train, y_test = train_test_split(struc_w2index, y, test_size=self.test_size)
        #print(y_train, y_test)
        # 分类标签-1,0,1转化为0,1,2
        encoder = LabelEncoder()
        encoded_y_train = encoder.fit_transform(y_train)
        encoded_y_test = encoder.fit_transform(y_test)
        #print(encoded_y_train,encoded_y_test)
        # one-hot编码：-1=0=[1. 0. 0]; 0=1=[0. 1. 0.]; 1=2=[0. 0. 1.]
        y_train = np_utils.to_categorical(encoded_y_train)
        y_test = np_utils.to_categorical(encoded_y_test)
        #print (y_train,y_test)     
        return n_symbols,embedding_weights,x_train,y_train,x_test,y_test
    
    
    # 定义网络结构
    def train_lstm(self,n_symbols,embedding_weights,x_train,y_train,x_test,y_test):
        nb_classes=3
        print ('Defining a Simple Keras Model...')
        model = Sequential()  
        model.add(Embedding(output_dim=self.vocab_dim, # 每个词的词向量维度
                            input_dim=n_symbols, # 所有的词的长度加1
                            mask_zero=True,  # 确定是否将输入中的‘0’看作是应该被忽略的‘填充’（padding）值
                            weights=[embedding_weights], # 词向量矩阵                         
                            input_length=self.input_length))  # 当输入序列的长度固定时，该值为其长度
        
        '''二分类
        ### keras层的参数设置
        model.add(LSTM(output_dim=50, activation='sigmoid', inner_activation='hard_sigmoid'))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))
        print ('Compiling the Model...')
        model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
        '''
    
        # 三分类
        ## 使用单层LSTM 输出的向量维度是50，输入的向量维度是vocab_dim,激活函数relu
        model.add(LSTM(output_dim=50, activation='relu', inner_activation='hard_sigmoid'))
        model.add(Dropout(0.5))
        ## 在这里外接softmax，进行最后的3分类
        model.add(Dense(output_dim=nb_classes, input_dim=50, activation='softmax'))
        
        # 开始训练 
        print ('Compiling the Model...')
        model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])       
        print ("Train...")    
        model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.n_epoch,\
                      verbose=1, validation_data=(x_test, y_test))
        print ("Evaluate...")
        score = model.evaluate(x_test, y_test,batch_size=self.batch_size)
        yaml_string = model.to_yaml()
        with open(self.lstm_model, 'w') as outfile:
            outfile.write( yaml.dump(yaml_string, default_flow_style=True) )
        model.save_weights(self.lstm_weight)
        print ('Test score:', score)
    
    
    # 训练模型，并保存
    def train(self):              
        print ('Loading train Data...')       
        combined,y=self.load_train_file() # combined是正、中性、负样本,y是标签 
        print ('Tokenising...')
        combined = self.tokenizer(combined)   #tokenizer()是分词并处理空格的函数 
        print(len(combined))
        print ('Training a Word2vec model...')       
        w2indx,w2vec,struc_w2index=self.train_data_struc(combined)     
        print ('Setting up Arrays for Keras Embedding Layer...')
        n_symbols,embedding_weights,x_train,y_train,x_test,y_test=self.get_train_data(w2indx,w2vec,struc_w2index,y)
        
        
        print (x_train.shape,y_train.shape)
        self.train_lstm(n_symbols,embedding_weights,x_train,y_train,x_test,y_test)   
        

'''
mm=Lstm_nn()      
mm.train()
'''
        
        
        
        
        
        
        
        
        
        
        
        
        