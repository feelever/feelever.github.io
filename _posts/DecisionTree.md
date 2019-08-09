 # Decision Tree
通过设定条件来预测条件的一棵树
## 分类
* 分类树 输出是样本的类标
* 回归树 输出是一个实数
### 决策树算法
* CART
* ID3算法
* C4.5算法
* CHAID
* MARS 数值型
### 算法实例
* Bagging 用有放回抽样法来训练多棵决策树，最终结果用投票法产生
* Random Forest 使用多棵决策树来改进分类性能
* Boosting Tree 可以用来做回归分析和分类决策
* Rotation Forest 每棵树的训练首先使用主元分析法
## CART 分类
用于预测离散数据
公式:
    $$Gini(p)=\sum_{k=1}^{m}p_k(1-p_k)=1-\sum_{k=1}^{m}p_{k}^{2}$$
* k代表第k个分类，m为总分类数目，$p_k$为样本点属于第k类的概率
    $$Gini(D)=1-\sum_{k=1}^{k}(\frac{|C_k|}{|D|})^2$$
* D代表集合样本$C_k$代表属于第k类的样本子集
$$Gain_Gini(D,A)=\frac{|D_1|}{D}Gini(D_1)+\frac{|D_2|}{D}Gini(D_2)$$
* A代表特征，a指取值
* $Gini(D)表示集合D的不确定性，Gini(D,A)$表示A=a分割后D集合不确定性
整个迭代最终取
    $$Min_{i\in A}(Gain_Gini(D,A))$$
    $$Min_{A\in attribute}(Min_{i\in A}(Gain_Gini(D,A)))$$
## CART 回归
用于预测连续型数据
设
$$D={(x_1,y_1),...(x_n,y_n)}$$
* x为输入，y为输出，且y为连续表达式
$$f(x)=\sum_{m=1}^{m}C_mI(x\in R_m)$$
其中$C_m$为$R_m$对应的固定输出值
$R_m$: $$R_1(j,s)={x|x^j\leq s},R_2(j,s)={x|x^j>s}$$
$C_m$: $$\frac{1}{N_m}\sum_{x_i\in R_m(j,s)}y_i$$
* j代表变量，s为切分点（j,s）对选取如下：
$$Min_(j,s)[Min_{c_1}\sum_{x_i\in R_i(j,s)}(y_i,C_1)^2+Min_{c_2}\sum_{x_i\in R_i(j,s)}(y_i,C_2)^2]$$
## CART剪枝
CART剪枝分为两部分，分别是生成子树序列和交叉验证
损失函数
$$C_\alpha(T)=C(T)+\alpha|T|$$
* T为任意子树，|T|为T的叶子节点树
* $\alpha$为权衡拟合程度与树的复杂度
* C(T)为预测误差，可以为方差或者Gini指数
当$\alpha$很小的时候T为最优子树
当$\alpha$很大的时候根节点就是最优子树
## 代码
决策树最经典的使用是鸢尾花数据集，sklearn代码如下:
```python
from sklearn.datasets import load_iris
from sklearn import tree

#load data
iris=load_iris()
X=iris.data
y=iris.target
clf=tree.DecisionTreeClassifier()
clf=clf.fit(X,y)

#export the decision tree
#graphviz需要安装工具，不同环境不通，反正brew,yum,apt,choco(windows上的包管理工具)
import graphviz
#export_graphviz support a variety of aesthetic options
dot_data=tree.export_graphviz(clf,out_file=None,
                              feature_names=iris.feature_names,
                              class_names=iris.target_names,
                              filled=True,rounded=True,
                              special_characters=True)

graph=graphviz.Source(dot_data)
graph.view()
```
## 相关
https://zh.wikipedia.org/wiki/%E5%86%B3%E7%AD%96%E6%A0%91%E5%AD%A6%E4%B9%A0
https://zhuanlan.zhihu.com/p/36108972