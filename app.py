import connect_sql,crawl_song,\
    edit_music,music_classify,visualization
import joblib
from tqdm import tqdm
# uid = 393361316

def get_musicclass(song_id,tag,start_time,end_time):
    save_name = "test.mp3"
    print("下载歌曲中...")
    crawl_song.download_song(save_name,song_id)
    print("下载完成")
    save_wav = "test.wav"
    print("类型转换...")
    fg = music_classify.mp3_to_wav(save_name,save_wav)
    if fg == True:
        print("类型转换成功")
    else:
        print("暂无版权或者需要vip特权")
        return None
    if tag == 2:
        print("裁剪wav....")
        edit_music.clip_music(save_wav,save_wav,start_time,end_time)
        print("裁剪wav成功")
    x_predict = []
    print("获取特征....")
    x_predict.append( music_classify.get_mfcc_feature(save_wav))
    print("获得特征")
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

if __name__ == '__main__':

    uid = "393361316"
    # user_data = sql.get_recoder_byUid(uid)
    # tag1_data = user_data.query("tag==1")
    # tag2_data = user_data.query("tag==2")
    # print(tag2_data)
    # get_musicclass("316686",0,0,0)
    download_user_music(uid)