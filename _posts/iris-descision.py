from sklearn.datasets import load_iris
from sklearn import tree

#load data
iris=load_iris()
X=iris.data
y=iris.target
clf=tree.DecisionTreeClassifier()
clf=clf.fit(X,y)

#export the decision tree
import graphviz
#export_graphviz support a variety of aesthetic options
dot_data=tree.export_graphviz(clf,out_file=None,
                              feature_names=iris.feature_names,
                              class_names=iris.target_names,
                              filled=True,rounded=True,
                              special_characters=True)
print(dot_data)
graph=graphviz.Source(dot_data)
graph.view()