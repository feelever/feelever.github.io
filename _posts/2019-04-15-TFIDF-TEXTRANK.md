# TF-IDF与TextRank
  
## TF-IDF
  
* Term Frequency - Inverse Document Frequency
* 通过词出现频率来对文章中某些词的权重进行评估
#### 公式
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?TF_{w,D_i}=%20&#x5C;frac{count(w)}{|D_i|}"/></p>  
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?IDF_w=log&#x5C;frac{N}{1+&#x5C;sum_{i=1}^{n}I(w,D_i)}"/></p>  
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?TF-IDF_{w,D_i}=TF_{w,D_i}&#x5C;cdot%20IDF_w"/></p>  
  
* 当一个词在文档频率越高并且新鲜度高（即普遍度低），其TF-IDF值越高
* TF-IDF兼顾词频与新鲜度，过滤一些常见词，保留能提供更多信息的重要词。
  
## TextRank
  
### #
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?PR(V_i)=(1-d)+d*&#x5C;sum_{j&#x5C;in%20In(V_i)}&#x5C;frac{1}{|Out(V_j)|}PR(V_j)"/></p>  
  
* <img src="https://latex.codecogs.com/gif.latex?PR(V_i)"/>代表<img src="https://latex.codecogs.com/gif.latex?V_i"/>rank值，<img src="https://latex.codecogs.com/gif.latex?In(V_i)"/>表示<img src="https://latex.codecogs.com/gif.latex?V_i"/>前驱集合，<img src="https://latex.codecogs.com/gif.latex?Out(V_j)"/>表示<img src="https://latex.codecogs.com/gif.latex?V_j"/>后继集合，<img src="https://latex.codecogs.com/gif.latex?d"/>代表damping factor做平滑
### #
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?WS(V_i)=(1-d)+d*&#x5C;sum_{j&#x5C;in%20In(V_i)}&#x5C;frac{W_ji}{&#x5C;sum_{V_k&#x5C;in%20Out(V_j)}w_{jk}}WS(V_j)"/></p>  
  
### #
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?Similarity(S_i,S_j)=&#x5C;frac{|{w_k(w_k&#x5C;in%20S_i%20&#x5C;,and%20&#x5C;,W_k&#x5C;in%20S_j)}|}{log(|S_i|)+log(s_j)}"/></p>  
  
* <img src="https://latex.codecogs.com/gif.latex?S_i,S_j"/>表示各自句子词总数
* <img src="https://latex.codecogs.com/gif.latex?W_k"/>表示句子中的词
  
#### 对比
  
* TF-IDF与TextRank都依赖于分词；
* TextRank考虑了词之间的关系，但是扔会将频繁词作为关键词
* TextRank涉及到topK的图计算，提取速度较慢
  
#### 实现步骤
  
1. 素材整合成文本数据
2. 文本分割成句子
3. 句子转换成向量表示为词向量（？）
4. 计算句子向量相似性并存放矩阵中
5. 将相似矩阵转换为句子为节点，相似性得分为边的图，用于计算文本评分
6. 最后，topN为文本摘要
  
#### 参考链接
  
https://www.jiqizhixin.com/articles/2018-12-28-18
  