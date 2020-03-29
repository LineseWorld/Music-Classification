# coding=utf-8,
import requests,json,connect_sql,os,random
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
true = True
false = False
null = None

# 网易云个人用户uid=393361316

# 获取单首歌歌词
def get_lrc(song_id):
    """
    根据id得到时间轴的歌词
    :param song_id:歌曲id
    :return:
    """
    url = 'http://localhost:3000/lyric?id='+str(song_id)
    html = requests.get(url).text
    dits = eval(html)
    if 'lrc' in dits.keys():
        tmp = dits["lrc"]
        lrc = tmp["lyric"]
    else:
        lrc=" "
    return lrc

# 转义
def change(s):
    """
    符号转义
    :param s: 带有 " ' 字符
    :return:
    """
    s=s.replace("'", "\\'")
    s=s.replace('"', '\\"')
    return s

# 批量下载歌单歌曲
def download_musiclist(Songs,filename,start,n):
    """
    下载 歌单中start到n 首音乐
    :param Songs:songlist
    :param filename:
    :param n:下载个数
    :return:
    """
    cnt = start
    for song in Songs:
        file_name = 'mp3file/'+filename+'/'+str(cnt)+".mp3"
        download_song(file_name,song["url"])
        cnt += 1
        if cnt >= n:
            break

# 批量下载歌单歌词
def download_lrc(Songs):
    """
    下载歌词
    :param Songs:
    :return:
    """
    for song in Songs:
        song_id = song["id"]
        lrc = get_lrc(song_id)
        print("id:",song_id,"lrc:\n",lrc)
        file_name = 'lrcfile/'+str(song_id)+".txt"
        with open(file_name,'w',encoding='utf-8') as file:
            file.write(lrc)
            file.close()

# 判断是否拥有mp3版权
def judge_song_url(song_id):
    """
    判断音乐是否存在
    :param song_id:
    :return:
    """
    url = "http://localhost:3000/check/music?id="+str(song_id)
    html = requests.get(url).text
    dict=eval(html)
    return dict["success"]

# 得到歌单
def get_songlist(listid,n):
    """
    根据歌单id得到歌曲列表
    :param listid:
    :param n:
    :return:
    """
    url = 'http://music.163.com/api/playlist/detail?id='+str(listid)
    html = requests.get(url,headers=headers).text
    dits = eval(html)

    dits = dits["result"]
    dits = dits["tracks"]
    songs=[]
    cnt = 0
    for songmess in dits:
        song_id = str(songmess["id"])
        if judge_song_url(song_id) == False:
            continue;
        song_name = songmess["name"]
        song_name = change(song_name) # 转义
        song_author = songmess["artists"]
        song_author = song_author[0]
        song_author = song_author["name"]
        song_url = "http://music.163.com/song/media/outer/url?id=" + song_id + ".mp3"
        song_lrc = get_lrc(song_id)
        songs.append({
                "song_id":song_id,
                "song_name":song_name,
                "song_author":song_author,
                "song_lrc":song_lrc,
                "song_url":song_url
        })
        cnt+=1
        if cnt >= n:
            break

    print(cnt)
    return songs

# 下载歌曲
def download_song(save_name,song_id):
    """
    下载单曲
    :param save_name:保存路径
    :param song_id:歌曲id
    :return:
    """
    if judge_song_url(song_id)==False:
        print("无歌曲版权")
    else:
        song_url="http://music.163.com/song/media/outer/url?id="+str(song_id)+".mp3"
        res = requests.get(song_url, headers=headers)
        music = res.content
        with open(file_name, 'wb') as file:
            file.write(music)
            file.flush()
            file.close()

# 计算文件数量
def count_files(path):
    """
    判断文件数量
    :param path:文件夹路径
    :return:
    """
    list = os.listdir(path)
    print(len(list))

# 得到用用户播放记录
def get_user_recoder(uid,n,type):
    """
    查看用户播放记录
    :param uid: 用户id
    :param n: 前n个记录
    :param type: 0 表示所有记录，1表示一周的记录
    :return: 返回记录列表
    """
    url = "http://localhost:3000/user/record?uid="+str(uid)+"&type="+str(type)
    html = requests.get(url).text
    dits = eval(html)
    if type == 1:
        dits = dits["weekData"]
    if type == 0:
        dits = dits["allData"]
    user_recoder=[]
    cnt = 0
    for message in dits:
        playcount = message["playCount"]
        # print("playCount: ",playcount)
        song = message["song"]
        song_id = song["id"]
        song_name = song["name"]
        print(song_name)
        user_recoder.append({
            "uid" : str(uid),
            "song_id": song_id,
            "tag":1,
            "start":0,
            "end":0,
            "times":random.randint(1,15),# 随机数生成播放次数
            "message":change(song_name)
        })
        cnt+=1
        if cnt>n:
            break
    print("爬取歌曲数量: ",cnt)
    return user_recoder


if __name__ == '__main__':
    print("crawl_song")





