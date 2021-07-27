# BooleanSearch


- [BooleanSearch](#booleansearch)
  - [Description](#description)
  - [Modules](#modules)
  - [Results](#results)



## Description
实验通过基于 MapReduce 方法实现对新闻文本数据的布尔查询系统。新闻数据集来自 [搜狗全网新闻数据 SogouCA 2012版本(1.43GB)](http://www.sogou.com/labs/resource/ca.php) 来自若干新闻站点2012年6月—7月期间国内，国际，体育，社会，娱乐等18个频道的新闻数据，提供URL和正文信息。数据格式如下：
```
<doc>
<url>页面 URL</url>
<docno>页面 ID</docno>
<contenttitle>页面标题 </contenttitle>
<content>页面内容 </content>
</doc>
注意：content字段去除了HTML标签，保存的是新闻正文文本
```
将原始的数据信息经过前处理，包含提取相关信息、分词、去除停用词等，通过 MapReduce 方法对文档建立倒排索引，实现对新闻的布尔查询。


## Modules
- [```main.py```](https://github.com/Aman-4-Real/BooleanSearch/blob/main/src/main.py): 

作为程序入口，主要包含各功能的串接，运行后会调用相应模块建立索引。

- [```MapReduce.py```](https://github.com/Aman-4-Real/BooleanSearch/blob/main/src/MapReduce.py): 

通过MapReduce方法建立索引构建了MapReduce类。由于文本数据较大，通过python中带有的multiprocessing库实现程序的并行化操作，以提高程序的运行效率，缩短程序的运行时间。

生成倒排索引表包含以下步骤：
- 对新闻数据进行清洗，只提取其中的<content>部分。
- 对该部分进行分词处理，并计算各条新闻中各词的次数。同时记录各个词对应出现在文件的行数。
- 对所有新闻的所有词次数进行统计，保存在指定大小的词典集中。
- 通过得到的词语对应的新闻所在行数的倒排索引表，保存为```.pkl```索引文件用于检索模块。

- [```MultiProcess.py```](https://github.com/Aman-4-Real/BooleanSearch/blob/main/src/MultiProcess.py): 

包含对文件的拆分，分词去停用词等预处理，以及Map和Reduce的实现。

- [```search.py```](https://github.com/Aman-4-Real/BooleanSearch/blob/main/src/search.py): 

检索部分的串联模块包含调取相关函数、数据索引的读取、以及检索界面和结果的
显示。

- [```retrival.py```](https://github.com/Aman-4-Real/BooleanSearch/blob/main/src/retrival.py): 

检索部分的实现模块。将输入的查询进行分词处理，作为关键词进行查询。将多个关键词按照布尔查询的方法，根据索引取出序列，按照序列长度进行排序，然后从短序列卡开始合并直至获得最终的目标文本序列。最后通过索引在源新闻数据中将新闻检索出来。


## Results

![1](https://github.com/Aman-4-Real/BooleanSearch/blob/main/imgs/1.jpg)
![2](https://github.com/Aman-4-Real/BooleanSearch/blob/main/imgs/2.png)
![3](https://github.com/Aman-4-Real/BooleanSearch/blob/main/imgs/3.png)
![4](https://github.com/Aman-4-Real/BooleanSearch/blob/main/imgs/4.png)



