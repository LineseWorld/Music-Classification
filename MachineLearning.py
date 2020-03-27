from sklearn.datasets import  load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier,export_graphviz

"""
机器学习初步学习代码
"""
def knn_iris():
    """
    用KNN算法鸢尾花进行分类
    :return:
    """
    # 1 获取数据
    iris  =load_iris()

    # 2 划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=6)

    # 3 特征工程 标准化处理
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4 KNN 算法预估
    estimator  = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train,y_train)

    # 5 模型评估
    # 方法1 直接比较
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("真实值和预测值：\n",y_test == y_predict)
    # 方法2：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    return None

def knn_iris_gscv():
    """
    用KNN算法鸢尾花进行分类,添加网格搜索和交叉验证
    :return:
    """
    # 1 获取数据
    iris  =load_iris()

    # 2 划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=6)

    # 3 特征工程 标准化处理
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    # 4 KNN 算法预估
    estimator  = KNeighborsClassifier()
    # 加入网格搜索和交叉验证
    # 参数准备
    param_dict = {"n_neighbors":[1,3,5,7,9]}
    estimator = GridSearchCV(estimator,param_grid=param_dict,cv=10)
    estimator.fit(x_train,y_train)


    # 5 模型评估
    # 方法1 直接比较
    y_predict = estimator.predict(x_test)
    print("y_predict:\n",y_predict)
    print("真实值和预测值：\n",y_test == y_predict)
    # 方法2：计算准确率
    score = estimator.score(x_test,y_test)
    print("准确率为：\n",score)

    # 最佳参数：best_params_
    print("最佳参数:\n",estimator.best_params_)
    # 最佳结果: best_score
    print("最佳结果:\n",estimator.best_score_)
    # 最佳估计器: best_estimator_
    print("最佳估计器:\n", estimator.best_estimator_)
    # 交叉验证结果 cv_results_
    print("交叉验证结果:\n", estimator.cv_results_)

    return None


def decision_iris():
    """
    用决策数对鸢尾花进行分类
    :return:
    """
    # 1 数据获取
    iris = load_iris()
    # 2 划分数据集
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,random_state=6)
    # 3 使用决策树分类器
    estimator =  DecisionTreeClassifier(criterion="entropy")
    estimator.fit(x_train,y_train)
    # 4 模型评估
    # 方法1 直接比较
    y_predict = estimator.predict(x_test)
    print("y_predict:\n", y_predict)
    print("真实值和预测值：\n", y_test == y_predict)
    # 方法2：计算准确率
    score = estimator.score(x_test, y_test)
    print("准确率为：\n", score)

    # 可视化决策树
    export_graphviz(estimator,out_file="iris_tree.dot",feature_names=iris.feature_names)



if __name__ == "__main__":
    # print("==============")
    # 代码1 ： 用KNN算法鸢尾花进行分类
    # knn_iris()
    # print("==============")
    # 代码2 ： 用KNN算法鸢尾花进行分类 添加网格搜索和交叉验证
    # knn_iris_gscv()
    print("==============")
    # 代码3 :  用决策数对鸢尾花进行分类
    decision_iris()
