#TF-IDF与TextRank
##TF-IDF
* Term Frequency - Inverse Document Frequency
* 通过词出现频率来对文章中某些词的权重进行评估
#### 公式
$$TF_{w,D_i}= \frac{count(w)}{|D_i|}$$
$$IDF_w=log\frac{N}{1+\sum_{i=1}^{n}I(w,D_i)}$$
$$TF-IDF_{w,D_i}=TF_{w,D_i}\cdot IDF_w$$
* 当一个词在文档频率越高并且新鲜度高（即普遍度低），其TF-IDF值越高
* TF-IDF兼顾词频与新鲜度，过滤一些常见词，保留能提供更多信息的重要词。
  
##TextRank
####
$$PR(V_i)=(1-d)+d*\sum_{j\in In(V_i)}\frac{1}{|Out(V_j)|}PR(V_j)$$
* $PR(V_i)$代表$V_i$rank值，$In(V_i)$表示$V_i$前驱集合，$Out(V_j)$表示$V_j$后继集合，$d$代表damping factor做平滑
####
$$WS(V_i)=(1-d)+d*\sum_{j\in In(V_i)}\frac{W_ji}{\sum_{V_k\in Out(V_j)}w_{jk}}WS(V_j)$$
####
$$Similarity(S_i,S_j)=\frac{|{w_k(w_k\in S_i \,and \,W_k\in S_j)}|}{log(|S_i|)+log(s_j)}$$
* $S_i,S_j$表示各自句子词总数
* $W_k$表示句子中的词

####对比
* TF-IDF与TextRank都依赖于分词；
* TextRank考虑了词之间的关系，但是扔会将频繁词作为关键词
* TextRank涉及到topK的图计算，提取速度较慢

####实现步骤
1. 素材整合成文本数据
2. 文本分割成句子
3. 句子转换成向量表示为词向量（？）
4. 计算句子向量相似性并存放矩阵中
5. 将相似矩阵转换为句子为节点，相似性得分为边的图，用于计算文本评分
6. 最后，topN为文本摘要
   
####参考链接
https://www.jiqizhixin.com/articles/2018-12-28-18