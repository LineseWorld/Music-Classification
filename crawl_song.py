# coding=utf-8,
import requests,json,connect_sql,os,random
from bs4 import BeautifulSoup


# 网易云个人用户uid=393361316
# 歌曲类型歌单
# 流行 3136952023 3172849329
# 摇滚 2538096700
# 民谣 979321026
# 电子 2557744972 2829839197
# 说唱 2246886256
def search_song_byid(id):
    """
    根据歌曲id 得到歌曲信息
    :param id:
    :return: song_id song_name song_author song_lrc
    """
    url = 'http://localhost:3000/song/detail?ids='+id
    html = requests.get(url).text
    true = True
    false = False
    null = None
    dits = eval(html)
    dits = dits["songs"]
    song_lrc = get_lrc(id)
    # 解决引号字符问题
    song_lrc = song_lrc.replace("'","\\'")
    song_lrc = song_lrc.replace('"', '\\"')
    # print(dits)
    dits=dits[0]
    song_name = dits["name"]
    dits = dits["ar"]
    # print(dits)
    dits = dits[0]
    song_author = dits["name"]
    # print(song_author)
    song=[]
    song.append(id)
    song.append(song_name)
    song.append(song_author)
    song.append(0)
    song.append(song_lrc)
    # print(song)
    return song



def get_lrc(song_id):
    """
    根据id得到时间轴的歌词
    :param song_id:
    :return:
    """
    url = 'http://localhost:3000/lyric?id='+song_id
    html = requests.get(url).text
    true = True
    false = False
    null = None
    dits = eval(html)
    if 'lrc' in dits.keys():
        tmp = dits["lrc"]
        lrc = tmp["lyric"]
    else:
        lrc=" "
    return lrc

def change(s):
    """
    符号转义
    :param s:
    :return:
    """
    s=s.replace("'", "\\'")
    s=s.replace('"', '\\"')
    return s

def get_songlist(listid):
    """
    爬取网易云歌单和mp3文件
    :return:
    """
    url = 'https://music.163.com/playlist?id='+listid
    # 请求HTML
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    alist = soup.select("a")
    Songs = []
    for music in alist:
        if music.has_attr("href"):
            if str(music.attrs["href"]).startswith("/song?id="):
                id = str(music.attrs["href"]).replace("/song?id=", "")
                print("id:",id)
                if id[0] == '$':
                    break
                Songs.append({
                    "id": id,
                    "url": "http://music.163.com/song/media/outer/url?id=" + id + ".mp3",
                    "name": music.text
                })
    return Songs

def download_music(Songs,filename,start):
    """
    下载音乐
    :param Songs:
    :param filename:
    :param start:
    :return:
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    id = start
    for song in Songs:
        print(song["name"])
        res = requests.get(song["url"],headers=headers)
        music = res.content
        file_name = 'mp3file/'+filename+'/'+str(id)+".mp3"
        print("写入%d文件" % id)
        id+=1
        with open(file_name,'wb') as file:
            file.write(music)
            file.flush()
            file.close()
        if id >= 150:
            break

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

def judge_song_url(song_id):
    """
    判断音乐是否存在
    :param song_id:
    :return:
    """
    url = "http://localhost:3000/check/music?id="+str(song_id)
    html = requests.get(url).text
    true = True
    false = False
    null = None
    print(html)
    dict=eval(html)
    return dict["success"]

def get_songlist(listid,n):
    """
    根据歌单id得到歌曲列表
    :param listid:
    :param n:
    :return:
    """
    url = 'http://music.163.com/api/playlist/detail?id='+str(listid)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    html = requests.get(url,headers=headers).text

    true = True
    false = False
    null = None
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
        print(song_name)
        song_author = songmess["artists"]
        song_author = song_author[0]
        song_author = song_author["name"]
        song_url = "http://music.163.com/song/media/outer/url?id=" + song_id + ".mp3"
        song_lrc = get_lrc(song_id)
        songs.append({
                "id":song_id,
                "name":song_name,
                "author":song_author,
                "lrc":song_lrc,
                "url":song_url
        })
        cnt+=1
        if cnt >= n:
            break

    print(cnt)
    return songs

def download_one_song(file_name,song_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
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

def count_files(path):
    list = os.listdir(path)
    print(len(list))


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

    true = True
    false = False
    null = None
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
    print("----")
    # recoder = get_user_recoder(393361316,1000,0)
    songlist = get_songlist(558424255,1000)




