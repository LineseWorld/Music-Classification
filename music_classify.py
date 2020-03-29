from pydub import AudioSegment
import wave,csv,os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from scipy import fft
from scipy.io import wavfile
from tqdm import tqdm
import librosa
from sklearn import svm
from sklearn.externals import joblib

"""
实现音乐分类器
"""
# mp3转为wav
def mp3_to_wav(file_name,save_name):
    """
    将单个mp3文件转为wav格式
    :param file_name: mp3路径
    :param save_name: wav路径
    :return:
    """
    try:
        sound = AudioSegment.from_mp3(file_name)
        sound.export(save_name,format ='wav')
    except Exception as msg:
        print(msg)

# 得到mfcc特征变换向量
def get_mfcc_feature(path):
    """
    对wav做mfcc特征转换
    :param path: wav文件路径
    :return:
    """
    try:
        y, sr = librosa.load(path=path)
        # 提取mfcc 特征
        mfccs = librosa.feature.mfcc(y=y,sr=sr,n_mfcc=13)
        mf = np.mean(mfccs,axis=1)
        mc = np.cov(mfccs)
        result = mf
        for i in range(mfccs.shape[0]):
            result = np.append(result,np.diag(mc,i))
        return result
    except Exception as msg:
        print(msg)

# 将列表写入本地
def Save_list(list,filename):
    """
    将列表存储到本地
    :param list: 列表
    :param filename: 存储文件名
    :return:
    """
    with open(filename + '.txt', 'w') as file:
        for i in range(len(list)):
            for j in range(len(list[i])):
                file.write(str(list[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
                file.write('\t')                          # 相当于Tab一下，换一个单元格
            file.write('\n')                              # 写完一行立马换行
        file.close()

# 读取特征矩阵
def Read_list_x(filename):
    """
    读取特征矩阵
    :param filename:
    :return:
    """
    file1 = open(filename+".txt", "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
        list_source.append(column_list)                # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j]=float(list_source[i][j])
    file1.close()
    return list_source

# 读取目标值
def Read_list_y(filename):
    """
    读取目标值
    :param filename:
    :return:
    """
    file1 = open(filename+".txt", "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
        list_source.append(column_list)                # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j]=int(list_source[i][j])
    file1.close()
    ret = []
    for i in range(len(list_source)):
        for j in range(len(list_source[0])):
            ret.append(list_source[i][j])
    return ret

# 批量存储训练集特征
def save_feature():
    """
    存储mfcc特征矩阵
    :return:
    """
    genre_list = ['antique_music',
                  'classical_music',
                  'electronic_music',
                  'folk_music',
                  'pop_music',
                  'rap_music',
                  'rock_music']
    x_train = []
    y_train = []
    for g in tqdm(genre_list):
        print(g)
        for n in tqdm(range(150)):
            path = "wavfile/" + g + "/" + str(n) + ".wav"
            if judge_exist(path) == False:
                continue
            ar = get_mfcc_feature(path)
            x_train.append(ar)
            y_train.append([genre_list.index(g)])

    Save_list(x_train, "x_train")
    Save_list(y_train, "y_train")
    print("特征保存成功")

# 使用交叉验证和网格搜索寻找最优参数
def classify_mfcc():
    """
    使用mfcc特征
    交叉验证支持向量机
    得到最佳参数
    :return:
    """
    genre_list = ['antique_music',
                  'classical_music',
                  'electronic_music',
                  'folk_music',
                  'pop_music',
                  'rap_music',
                  'rock_music']
    x_train = []
    y_train = []
    # 前130做训练集
    for g in tqdm(genre_list):
        print(g)
        for n in tqdm(range(130)):
            path = "wavfile/"+g+"/"+str(n)+".wav"
            if judge_exist(path) == False:
                continue
            ar = get_mfcc_feature(g, n)
            x_train.append(ar)
            y_train.append(genre_list.index(g))


    x_test = []
    y_test = []
    print("===========")
    # 后20做测试集
    for g in tqdm(genre_list):
        print(g)
        for n in tqdm(range(130, 150)):
            path = "wavfile/" + g + "/" + str(n) + ".wav"
            if judge_exist(path) == False:
                continue
            ar = get_mfcc_feature(g, n)
            x_test.append(ar)
            y_test.append(genre_list.index(g))
    # 网络交叉验证
    parameters = {
        'kernel': ('linear', 'rbf', 'poly'),
        'C': [0.1, 1],
        'probability': [True, False],
        'decision_function_shape': ['ovo', 'ovr']
    }
    clf = GridSearchCV(svm.SVC(random_state=0), param_grid=parameters, cv=5)  # 固定格式
    print('开始交叉验证获取最优参数构建')
    clf.fit(x_train, y_train)
    print('最优参数：', end='')
    print(clf.best_params_)
    print('最优模型准确率：', end='')
    print(clf.best_score_)

    # 5 模型评估
    # 方法1 直接比较
    y_predict = clf.predict(x_test)
    print("y_predict:\n", y_predict)
    print("真实值和预测值：\n", y_test == y_predict)
    # 方法2：计算准确率
    score = clf.score(x_test, y_test)
    print("准确率为：\n", score)

# 保存最优svm分类器
def save_best_svm():
    """
    根据交叉验证得到的参数
    训练并存储最佳模型
    :return:
    """
    x_train = Read_list_x("x_train")
    y_train = Read_list_y("y_train")
    estimator = svm.SVC(C=0.1,decision_function_shape='ovo',kernel='linear',probability=True)
    estimator.fit(x_train,y_train)
    # 保存模型
    joblib.dump(estimator,'music_clf.pkl')

# 批量将mp3转为wav
def change_all_mp3():
    """
    将所有mp3文件转为wav
    :return:
    """
    file_list = ['antique_music',
                 'classical_music',
                 'electronic_music',
                 'folk_music',
                 'pop_music',
                 'rap_music',
                 'rock_music']
    for file in file_list:
        print("开始转换音乐类型",file)
        for i in range(150):

            file_name = "mp3file/"+file+"/"+str(i)+".mp3"
            save_name = "wavfile/"+file+"/"+str(i)+".wav"
            mp3_to_wav(file_name,save_name)
            print("转换成功 %s 中 %d .mp3" % (file,i) )

# 判断文件是否存在
def judge_exist(path):
    """
    判断文件是否存在
    :param path:
    :return:
    """
    return os.path.exists(path)

# 评估模型
def estimate_svm(x_test,y_test):
    """
    评价svm模型
    :param x_test:
    :param y_test:
    :return:
    """
    estimator = joblib.load("music_clf.pkl")
    score = estimator.score(x_test, y_test)
    print("准确率为：\n", score)

# 其他音乐分类方法
# def create_fit(g,n):
#     """
#     存储ftt特征矩阵
#     :param g:
#     :param n:
#     :return:
#     """
#     path = "F:/genres/genres/"+g+"/"+g+"."+str(n).zfill(5)+".wav"
#     # sample_rate:采样率，模数转换，X是音乐文件
#     sample_rate, X = wavfile.read(path)
#     # 用傅立叶变换处理1000HZ以下的数据
#     fft_features = abs(fft(X)[:2000])
#     sad = "trainset/"+g+"."+str(n).zfill(5)+".fft"
#     np.save(sad,fft_features)
#
# def do_fft():
#     """
#     将wav文件做fft转换
#     :return:
#     """
#     genre_list = ['blues','classcial','country','disco', 'rock','hiphop']
#     for g in genre_list:
#         for n in range(100):
#             create_fit(g, n)
#
# def logic_Classify():
#     """
#     使用逻辑回归实现音乐分类器
#     训练集数据来自generes 100首歌曲前30秒
#     :return:
#     """
#     genre_list = ['blues', 'rock']
#     x_train = []
#     y_train = []
#     # 前80做训练集
#     for g in tqdm(genre_list):
#         for n in range(90):
#             path = "trainset/" + g + "." + str(n).zfill(5) + ".fft.npy"
#             fft_features = np.load(path)
#             x_train.append(fft_features)
#             y_train.append(genre_list.index(g))
#
#     # 创建数组
#     x_train = np.array(x_train)
#     y_train = np.array(y_train)
#
#
#     x_test = []
#     y_test = []
#     # 后20做测试集
#     for g in tqdm(genre_list):
#         for n in range(90, 100):
#             path = "trainset/" + g + "." + str(n).zfill(5) + ".fft.npy"
#             fft_features = np.load(path)
#             x_test.append(fft_features)
#             y_test.append(genre_list.index(g))
#
#     # 创建数组
#     x_test = np.array(x_test)
#     y_test = np.array(y_test)
#
#     # 训练
#     # solver参数决定了我们对逻辑回归损失函数的优化方法
#     # sag 随机平均梯度下降
#     # multi_class OvR 多元逻辑回归看做二元逻辑回归
#     estimator = LogisticRegression(solver='sag')
#     estimator.fit(x_train, y_train)
#
#     # 模型评估
#     # 直接比较
#     y_predict = estimator.predict(x_test)
#     print("y_predict:\n", y_predict)
#     print("真实值和预测值：\n", y_test == y_predict)
#     # 计算准确率
#     score = estimator.score(x_test, y_test)
#     print("准确率为：\n", score)
#     print("训练评分：\n", estimator.score(x_train, y_train))
#
# def knn_Classify():
#     """
#     数据集为genres
#     KNN算法实现音乐分类器 准确率较低
#     :return:
#     """
#     genre_list = ['blues', 'rock']
#     x_train = []
#     y_train = []
#     # 前90做训练集
#     for g in tqdm(genre_list):
#         for n in range(90):
#             path = "trainset/" + g + "." + str(n).zfill(5) + ".fft.npy"
#             fft_features = np.load(path)
#             x_train.append(fft_features)
#             y_train.append(genre_list.index(g))
#
#     # 创建数组
#     x_train = np.array(x_train)
#     y_train = np.array(y_train)
#
#     x_test = []
#     y_test = []
#     # 后10做测试集
#     for g in tqdm(genre_list):
#         for n in range(90, 100):
#             path = "trainset/" + g + "." + str(n).zfill(5) + ".fft.npy"
#             fft_features = np.load(path)
#             x_test.append(fft_features)
#             y_test.append(genre_list.index(g))
#
#     # 创建数组
#     x_test = np.array(x_test)
#     y_test = np.array(y_test)
#
#     # 特征工程
#     transfer = StandardScaler()
#     x_train = transfer.fit_transform(x_train)
#     x_test = transfer.transform(x_test)
#
#     # KNN训练
#     estimator = KNeighborsClassifier()
#
#     # 加入网格搜索和交叉验证
#     # 参数准备
#     param_dict = {"n_neighbors": [5, 7, 9,11,13,15]}
#     estimator = GridSearchCV(estimator, param_grid=param_dict, cv=10)
#     estimator.fit(x_train, y_train)
#
#     # 模型评估
#     # 方法1 直接比较
#     y_predict = estimator.predict(x_test)
#     print("y_predict:\n", y_predict)
#     print("真实值和预测值：\n", y_test == y_predict)
#     # 方法2：计算准确率
#     score = estimator.score(x_test, y_test)
#     print("准确率为：\n", score)
#
#     # 最佳参数：best_params_
#     print("最佳参数:\n", estimator.best_params_)
#     # 最佳结果: best_score
#     print("最佳结果:\n", estimator.best_score_)
#     # 最佳估计器: best_estimator_
#     print("最佳估计器:\n", estimator.best_estimator_)
#     # 交叉验证结果 cv_results_
#     print("交叉验证结果:\n", estimator.cv_results_)

if __name__ == '__main__':
    x_test = Read_list_x("x_train")
    y_test = Read_list_y("y_train")






