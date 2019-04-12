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
* $PR(V_i)$代表$V_i$rank值，$In(V_i)$表示$V_i$前驱集合，$Out(V_j)$表示$V_j$后
