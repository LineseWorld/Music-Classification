import connect_sql,crawl_song,\
    edit_music,music_classify,visualization
import joblib
from tqdm import tqdm
import charts_tool as ct
# uid = 393361316

def get_musicclass(song_id):

    mfcc_file =  "E:\\musiclib\\mfcc\\"+str(song_id)+".txt"
    x_predict = music_classify.Read_list_x(mfcc_file)
    print("加载分类器")
    estimator = joblib.load("music_clf.pkl")
    print("加载完成")

    print("预测结果中....")
    y_predict = estimator.predict(x_predict)
    print("分类结果为：",y_predict)
    return y_predict

def download_user_music(user_id):
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    songdata = user_data.iloc[:,2:3]
    cnt = 0
    for row in songdata.itertuples():
        song_id=str(getattr(row, 'song_id'))
        if sql.judgesong(song_id) == None:
            print("下载中..",cnt)
            save_mp3 = "E:\\musiclib\\mp3\\"+str(song_id)+".mp3"

            fg1 = crawl_song.download_song(save_mp3,song_id)
            if fg1 == False:
                continue

            save_lrc = "E:\\musiclib\\lrc\\"+str(song_id)+".txt"
            crawl_song.download_lrc(save_lrc,song_id)

            save_wav = "E:\\musiclib\\wav\\"+str(song_id)+".wav"
            fg2 = music_classify.mp3_to_wav(save_mp3, save_wav)

            if fg2 == False:
                continue
            # print(song_id)
            cnt+=1
            sql.insert_song([song_id,'name','author','song_lrc','song_url'])
    print("cnt:",cnt)

def save_mfcc(song_id):
    target_wav = "E:\\musiclib\\wav\\"+str(song_id)+".wav"
    save_file  = "E:\\musiclib\\mfcc\\"+str(song_id)+".txt"
    if music_classify.judge_exist(save_file):
        print("已存在，不必进行特征转换")
        return
    x_predict = []
    x_predict.append(music_classify.get_mfcc_feature(target_wav))
    music_classify.Save_list(x_predict,save_file)


def save_predict(song_id):
    save_file = "E:\\musiclib\\predict\\" + str(song_id) + ".txt"
    if music_classify.judge_exist(save_file):
        print("已存在，不必进行特征转换")
        return
    y_predict = []
    y_predict.append(get_musicclass(song_id))
    music_classify.Save_list(y_predict, save_file)


def work_tag1_lrc(user_id,tag1_data):

    # 提取song_id
    song_ids = tag1_data.iloc[:,2:7]
    # print(song_ids)
    # 遍历
    for row in song_ids.itertuples():
        song_id = str(getattr(row, 'song_id'))
        times = getattr(row,'times')
        # 判断是否已存在于lrc文件夹中
        lrc_file = "E:\\musiclib\\lrc\\"+str(song_id)+".txt"
        if music_classify.judge_exist(lrc_file)==False:
            # 否-尝试进行下载
            crawl_song.download_lrc(lrc_file,song_id)
        # 是-拼接到用户词云txt
        user_lrc_file = "user_data/cloud_"+str(user_id)+".txt"
        for i in range(times):
            edit_music.write_to_file(lrc_file,0,10000,user_lrc_file);


def work_tag2_lrc(user_id,tag2_data):
    # 提取song_id
    song_ids = tag2_data.iloc[:, 2:7]
    # print(song_ids)
    # 遍历
    for row in song_ids.itertuples():
        song_id = str(getattr(row, 'song_id'))
        start_time = getattr(row,'start_time')
        end_time = getattr(row, 'end_time')
        times = getattr(row, 'times')
        # 判断是否已存在于lrc文件夹中
        lrc_file = "E:\\musiclib\\lrc\\" + str(song_id) + ".txt"
        if music_classify.judge_exist(lrc_file) == False:
            # 否-尝试进行下载
            crawl_song.download_lrc(lrc_file, song_id)
        # 是-拼接到用户词云txt
        user_lrc_file = "user_data/cloud_" + str(user_id) + ".txt"
        for i in range(times):
            edit_music.write_to_file(lrc_file, start_time, end_time, user_lrc_file)

def work_tag_plays(tag_data):
    """
    播放次数
    :param tag_data:
    :return:
    """
    ret = []
    for i in range(300):
        ret.append(0)
    cnt = 0
    data = tag_data.iloc[:,2:7]
    for row in data.itertuples():
        tag = getattr(row, 'tag')
        times = getattr(row, 'times')
        cnt += times
        if tag == 2:
            start_time = getattr(row,'start_time')
            end_time = getattr(row, 'end_time')
            for i in range(start_time,end_time):
                ret[i]+=times
    return (cnt,ret)

def work_tag_times(tag_data):
    """
    统计各类行为
    :param tag_data:
    :return:
    """
    data = tag_data.iloc[:, 2:7]
    res = 0
    for row in data.itertuples():
        times = getattr(row, 'times')
        res += times
    return res


def get_tag2_class(tag2_data):
    """
    音乐片段分类
    :param tag2_data:
    :return:
    """
    print("片段-音乐分类中....")
    result = [0,0,0,0,0,0,0,0]
    data = tag2_data.iloc[:,2:7]
    estimator = joblib.load("music_clf.pkl")
    for row in tqdm(data.itertuples()):
        song_id = str(getattr(row, 'song_id'))
        start_time = getattr(row, 'start_time')
        end_time = getattr(row, 'end_time')
        times = getattr(row, 'times')

        # 判断是否已存在于wav文件夹中
        wav_file = "E:\\musiclib\\wav\\" + str(song_id) + ".wav"
        mp3_file = "E:\\musiclib\\mp3\\" + str(song_id) + ".mp3"
        if music_classify.judge_exist(wav_file) == False:
            if music_classify.judge_exist(mp3_file) == False:
                # 否-尝试进行下载
                if crawl_song.download_song(mp3_file, song_id) == False:
                    continue
                if music_classify.mp3_to_wav(mp3_file, wav_file) == False:
                    continue
            else:
                if music_classify.mp3_to_wav(mp3_file, wav_file) == False:
                    continue
        edit_music.clip_music(wav_file,"clip.wav",start_time,end_time)
        x_predict = [music_classify.get_mfcc_feature("clip.wav")]
        y_predict = estimator.predict(x_predict)

        result[y_predict[0]]+=times


    return result

def get_class_other(tag_data):
    """
    音乐分类
    :param tag_data:
    :return:
    """
    print("其他-音乐分类中....")
    result = [0, 0, 0, 0, 0, 0, 0, 0]
    data = tag_data.iloc[:, 2:7]
    estimator = joblib.load("music_clf.pkl")
    for row in tqdm(data.itertuples()):
        song_id = str(getattr(row, 'song_id'))
        start_time = getattr(row, 'start_time')
        end_time = getattr(row, 'end_time')
        times = getattr(row, 'times')
        tag = getattr(row,'tag')
        if tag == 3:
            times = end_time/times
        elif tag == 4:
            times = times * 0.7

        # 判断是否已存在于wav文件夹中
        wav_file = "E:\\musiclib\\wav\\" + str(song_id) + ".wav"
        mp3_file = "E:\\musiclib\\mp3\\" + str(song_id) + ".mp3"
        predict_file = "E:\\musiclib\\predict\\" + str(song_id) + ".txt"
        mfcc_file = "E:\\musiclib\\mfcc\\" + str(song_id) + ".txt"

        if music_classify.judge_exist(predict_file) == True:
            y_predict = music_classify.Read_list_y(predict_file)
            result[y_predict[0]] += times
            continue

        if music_classify.judge_exist(mfcc_file) == True:
            x_predict = music_classify.Read_list_x(mfcc_file)
            y_predict = estimator.predict(x_predict)
            music_classify.Save_feature(y_predict,predict_file)
            result[y_predict[0]] += times
            continue

        if music_classify.judge_exist(wav_file) == False:
            if music_classify.judge_exist(mp3_file) == False:
                # 否-尝试进行下载
                if crawl_song.download_song(mp3_file, song_id) == False:
                    continue
                if music_classify.mp3_to_wav(mp3_file, wav_file) == False:
                    continue
            else:
                if music_classify.mp3_to_wav(mp3_file, wav_file) == False:
                    continue

        x_predict = [music_classify.get_mfcc_feature(wav_file)]
        y_predict = estimator.predict(x_predict)
        music_classify.Save_list(x_predict,mfcc_file)
        music_classify.Save_list(y_predict,predict_file)
        result[y_predict[0]] += times

    return result

def show_user_cloud(user_id):
    """
    用户词云
    :param user_id:
    :return:
    """
    print("开始绘制用户词云")
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")
    tag2_data = user_data.query("tag==2")
    work_tag1_lrc(user_id, tag1_data)
    work_tag2_lrc(user_id, tag2_data)
    user_lrc_file = "user_data/cloud_" + str(user_id) + ".txt"
    user_cloud_file = "user_data/cloud_" + str(user_id) + ".jpg"
    visualization.draw_cloud(user_lrc_file,user_cloud_file)
    # 数据清理
    with open(user_lrc_file,'w',encoding='utf-8') as f:
        f.write("")
        f.close()
    print("完成词云绘制")

def show_user_playhobby(user_id):
    """
    可视化播放习惯
    :param user_id:
    :return:
    """
    print("开始绘制用户听歌习惯")
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")
    tag2_data = user_data.query("tag==2")
    tag1_data = work_tag_plays(tag1_data)
    tag2_data = work_tag_plays(tag2_data)

    plays = [tag2_data[0],tag1_data[0]]
    playcounts = tag2_data[1]

    # visualization.pygal_line_playhobby(playcounts,user_id,"播放片段")
    # visualization.pygal_bar_plays(plays,user_id,"听歌方式")
    # visualization.pyga_pie_plays(plays,user_id,"听歌方式比重")
    ct.draw_line_clip(playcounts,user_id,"片段播放习惯")
    ct.draw_bar_plays(plays,user_id,"播放方式")
    print("完成播放方式绘制")


def show_user_class(user_id):
    """
    歌曲类别比重绘制
    :return:
    """
    print("开始绘制用户曲风偏爱")
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")  # 单曲循环
    tag2_data = user_data.query("tag==2")  # 片段播放
    tag3_data = user_data.query("tag==3")  # 评论时长+次数
    tag4_data = user_data.query("tag==4")  # 点赞评论
    tag5_data = user_data.query("tag==5")  # 收藏歌曲
    res = []
    res.append(get_class_other(tag1_data))
    res.append(get_tag2_class(tag2_data))
    res.append(get_class_other(tag3_data))
    res.append(get_class_other(tag4_data))
    res.append(get_class_other(tag5_data))
    result = [0,0,0,0,0,0,0]
    for item in res:
        for i in range(0,7):
            result[i]+=item[i]
    for i in range(0,7):
        result[i]=round(result[i],2)
    lable = ["古风","古典","电子","民谣","流行","说唱","摇滚"]
    data = []
    for i in range(0,7):
        data.append((lable[i],result[i]))
    # visualization.pyga_pie_class(result,user_id,"曲风偏爱比重")
    # visualization.pygal_bar_class(result,user_id,"收听曲风数据")
    ct.draw_pie_like(data,user_id)
    ct.draw_bar_like(data,user_id)
    print("完成曲风比重绘制")

def show_user_reconder(user_id):
    """
    行为占比绘制
    :param user_id:
    :return:
    """
    print("开始用户行为可视化")
    data = []
    lable = ["循环播放","片段播放","查看评论","点赞评论","收藏歌曲"]
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")  # 单曲循环
    data.append((lable[0],work_tag_times(tag1_data)))
    tag2_data = user_data.query("tag==2")  # 片段播放
    data.append((lable[1], work_tag_times(tag2_data)))
    tag3_data = user_data.query("tag==3")  # 评论时长+次数
    data.append((lable[2], work_tag_times(tag3_data)))
    tag4_data = user_data.query("tag==4")  # 点赞评论
    data.append((lable[3], work_tag_times(tag4_data)))
    tag5_data = user_data.query("tag==5")  # 收藏歌曲
    data.append((lable[4], work_tag_times(tag5_data)/10))
    ct.draw_bar_recoder(data,user_id)
    ct.draw_pie_recoder(data,user_id)
    print("完成行为可视化")



if __name__ == '__main__':
    uid = "393361316"
    # 代码一：词云绘制
    show_user_cloud(uid)

    # 代码二：偏爱绘制
    show_user_class(uid)

    # 代码三：方式绘制
    show_user_playhobby(uid)

    # 代码四：行为可视化
    show_user_reconder(uid)


