### 基于东方财富宏观研究的研报分类系统
东方财富宏观研究网址：http://data.eastmoney.com/report/hgyj.html

#### 代码结构
    一、该系统是由以下几步组成：
    （1）爬虫 （2）文本处理 （3）word2vec词向量训练 （4）Lstm模型训练 （5）基于模型的新文本预测
    
    二、运行该系统需要安装的包
    （1）爬虫中需要安装：selenium和PhantomJS，本人的安装环境是mac下的anaconda，安装过程可以参考：https://blog.csdn.net/lilong117194/article/details/83277075 （2）word2vec的训练过程，需要安装的包有jieba，这个包的安装很简单。 （3）lstm的训练过程，需要安装tensorflow和keras，mac下的安装也很简单
    
    三、各个.py文件的说明
    （1）reptile.py:爬虫文件 下面是各个函数的说明
    
    get_page_url(self,url,num)：模拟鼠标点击网页，获取指定页的网址。 参数url：网页地址，num：指定的网页数，也即是第几页，如下所示 在这里插入图片描述
    download_report(self,text_link,re_sum_info)：下载指定网页的研报文本。
    get_report_page(self,page_start,page_end)：以起始和终止页面数为爬取标准
    get_report_date(self,start_date,end_date)：以起始和终止时期为爬取标准
    （2）del_Ds_store.py：辅助文件，该文件的作用是删除mac系统下自动生成的.Ds_store文件，不去除的话会影响文本处理（windows下不会生成该文件）。 （3）filename_mod.py：辅助文件，该文件的作用是给新增的人工打标签重新命名，然后加入打过标签的文本库。 （4）interface.py：接口文件，即其他文件会调用该文件的函数
    
    __init__(self)：大部分的参数调整都在这里
    tokenizer(self,text)：对文本分词并去掉空格
    load_w2v_file(self,w2v_file_path)：加载训练文件
    text_proce(self,text_raw)：# 对文本进行处理
    file_test_vec(self,w2indx,file_reshape)：测试文本的向量化
    （5）word2vec.py：词向量训练文件
    
    word2vec_train(self,combined)：词向量训练
    create_dictionaries(self,model=None,combined=None)：创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
    test(self)：该文件仅做测试用 （6）lstm.py：lstm模型的训练
    splice_data(self,path)：该函数初步处理训练数据
    load_train_file(self)：拼接训练文件和文件的标签
    parse_dataset(self,combined)：得到每篇文本在词典中的索引列表
    train_data_struc(self,combined)：lstm模型训练数据的结构化
    get_train_data(self,word_index,word_vectors,struc_w2index,y): index_dict:所有的词索引列表(词：索引), word_vectors:所有词的词向量, combined:所有文本的索引值。该函数得到的结果才是用于lstm网络结构的结构化数据
    train_lstm：网络训练函数，网络的参数也是在这里调试。
    （7）main_test.py：这里是总的调用，爬虫、词向量训练、lstm模型训练、新文本预测都是在这个文件里。
    
    （8）terminal.py：该文件主要是预测新文本分类，也是最简单的接口调用。
    
    四、各个文件夹的说明
    spider_report：该文件夹下是爬取的6000个研报文本，主要用于词向量的训练。 word2vec_model：是word2vec训练保存的数据和模型 train_data：用于进行lstm训练的打过标签的文本 lstm_model：是lstm训练保存的数据和模型 test_report：爬取的用于预测的文本 测试代码：辅助处理文本的一些代码。
    
    
#### 安装包bug说明
    （1）mac 下安装homebrew: https://www.jianshu.com/p/e0471aa6672d?utm_campaign=hugo
    （2）mac brew install卡住： https://www.jianshu.com/p/f7cb08c50707
    （3）mac 安装npm：  brew install node
        报错参考
            * https://zhuanlan.zhihu.com/p/64125228
            * https://www.freesion.com/article/1914390492/
            * https://blog.csdn.net/guo_qiangqiang/article/details/104211087
    （4）"Selenium Python Headless Webdriver (PhantomJS) Not Working"
         https://stackoverflow.com/questions/54133200/phantomjs-with-selenium-message-phantomjs-executable-needs-to-be-in-path
     (5) Mac安装Chromedriver
        https://www.jianshu.com/p/a9df5135a3a3
     (6) mac下anaconda安装selenium+PhantomJS
        https://blog.csdn.net/lilong117194/article/details/83277075?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-3.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-3.nonecase
     (7) 无法打开“chromedriver”，因为无法验证开发者。
        https://www.cnblogs.com/may18/p/15237666.html