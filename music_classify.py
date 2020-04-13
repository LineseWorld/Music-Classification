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

import joblib
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
        return True
    except Exception as msg:
        print("vip特权")
        return False

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
    with open(filename, 'w') as file:
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
    file1 = open(filename, "r")
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
    file1 = open(filename, "r")
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

    Save_list(x_train, "x_train.txt")
    Save_list(y_train, "y_train.txt")
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


if __name__ == '__main__':
    x_test = Read_list_x("x_train.txt")
    y_test = Read_list_y("y_train.txt")






