import connect_sql,crawl_song,\
    edit_music,music_classify,visualization
import joblib
from tqdm import tqdm
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
        times = getattr(row, 'start_time')
        # 判断是否已存在于lrc文件夹中
        lrc_file = "E:\\musiclib\\lrc\\" + str(song_id) + ".txt"
        if music_classify.judge_exist(lrc_file) == False:
            # 否-尝试进行下载
            crawl_song.download_lrc(lrc_file, song_id)
        # 是-拼接到用户词云txt
        user_lrc_file = "user_data/cloud_" + str(user_id) + ".txt"
        for i in range(times):
            edit_music.write_to_file(lrc_file, start_time, end_time, user_lrc_file)

def show_user_cloud(user_id):
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

def work_tag_plays(tag_data):
    ret = []
    for i in range(300):
        ret.append(0)
    cnt = 0
    data = tag_data.iloc[:,2:7]
    # print(data)
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


def show_user_playhobby(user_id):
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")
    tag2_data = user_data.query("tag==2")
    tag1_data = work_tag_plays(tag1_data)
    tag2_data = work_tag_plays(tag2_data)
    # print(tag1_data)
    # print(tag2_data)
    plays = [tag2_data[0],tag1_data[0]]
    playcounts = tag2_data[1]

    visualization.pygal_line_playhobby(playcounts,user_id,"播放片段")
    visualization.pygal_bar_plays(plays,user_id,"听歌方式")
    visualization.pyga_pie_plays(plays,user_id,"听歌方式比重")


def show_user_data(user_id):
    sql = connect_sql.SQL()
    user_data = sql.get_recoder_byUid(user_id)
    tag1_data = user_data.query("tag==1")
    tag2_data = user_data.query("tag==2")
    show_user_playhobby(user_id)
    # work_tag1_lrc(user_id,tag1_data)
    # work_tag2_lrc(user_id,tag2_data)

if __name__ == '__main__':

    uid = "393361316"
    # user_data = sql.get_recoder_byUid(uid)
    # tag1_data = user_data.query("tag==1")
    # tag2_data = user_data.query("tag==2")
    # print(tag2_data)
    # get_musicclass("316686",0,0,0)
    # download_user_music(uid)
    # save_mfcc(108242)
    # x_predict =  music_classify.Read_list_x("E:\\musiclib\\mfcc\\108242.txt")
    # print(x_predict)
    # sql = connect_sql.SQL()
    # song_ids  = sql.get_songtabel()
    # for i in tqdm(song_ids):
    #     song_id = i[0]
    #     save_predict(song_id)
    show_user_data(393361316)

