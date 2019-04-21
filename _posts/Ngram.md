#N-gram
##基本解释
1. 基于统计语言模型，以N为滑动窗口对文本进行分片成gram的片段序列
2. 对生成的gram进行按照设定的阈值（？）频度统计，形成关键gram列表，
 形成该文本的特征向量，gram即为该文本的一个特征向量维度
3. 基于假设：第N个词出现只与前面N-1个词相关，完整的句子概率就是各个词
   出现概率的乘积；
##
$$p(w_1,w_2,...,w_m)=p(w_1)\cdot p(w_1|w_2) \cdot p(w_3|w_1,w_2)...p(w_m|w_1,..,w_{m-1})$$
=马尔可夫化=>
$$p(w_1,w_2,....,w_m)=p(w_i|w_{i-n+1,....w_{i-1}})$$
##一元模型
$$p(w_1,w_2,...w_m)=\prod_{i=1}^mP(w_i)$$
##二元模型
$$p(w_1,w_2,...w_m)=\prod_{i=1}^mP(w_i|w_{i-1})$$
##三元模型
$$p(w_1,w_2,...w_m)=\prod_{i=1}^mP(w_i|w_{i-2}w_{i-1})$$
### 
* M为词数量，$c(w_i)$表示出现次数
* unigram model
$$p(w_i)=\frac{C(w_i)}{M}$$
* 对于bigram model
$$p(w_i|w_{i-1})=\frac{C(w_{i-1}w_i)}{C(w_{i-1})}$$
* ngram model
$$p(w_i|w_{i-n-1},...,w_{i-1})=\frac{C(w_{i-n-1},...,w_i)}{C(w_{i-n-1},...w_{i-1})}$$

##学习资料
https://blog.csdn.net/baimafujinji/article/details/51281816